// map_screen.dart
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';

import 'package:http/http.dart' as http;
class MapScreen extends StatefulWidget {
  final LatLng? initialLocation;

  MapScreen({this.initialLocation});

  @override
  _MapScreenState createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late GoogleMapController mapController;
  LatLng? currentLocation;

  @override
  void initState() {
    super.initState();
    currentLocation = widget.initialLocation;
    if (currentLocation == null) {
      _getLocation();
    }
  }

  Future<void> _getLocation() async {
    LocationPermission permission = await Geolocator.requestPermission();
    if (permission == LocationPermission.denied ||
        permission == LocationPermission.deniedForever) {
      print("Location permissions denied");
      return;
    }

    Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high);
    setState(() {
      currentLocation = LatLng(position.latitude, position.longitude);
    });

    // Send location to backend (if needed)
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/location'),
      body: {
        'latitude': position.latitude.toString(),
        'longitude': position.longitude.toString(),
      },
    );
    print("Backend response: ${response.body}");
  }

  @override
  Widget build(BuildContext context) {
    return currentLocation == null
        ? Center(child: CircularProgressIndicator())
        : GoogleMap(
      onMapCreated: (controller) {
        mapController = controller;
      },
      initialCameraPosition: CameraPosition(
        target: currentLocation!,
        zoom: 14.0,
      ),
      myLocationEnabled: true,
    );
  }
}