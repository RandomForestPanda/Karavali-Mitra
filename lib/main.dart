/*
import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  GoogleSignIn _googleSignIn = GoogleSignIn(scopes: ['email'],clientId: '807837243380-ku6eat428jbumbo5dkovndj7lp3h9t8f.apps.googleusercontent.com',);
  bool isSignedIn = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Google OAuth Login")),
      body: Center(
        child: isSignedIn
            ? HomeScreen()
            : ElevatedButton(
          onPressed: () async {
            try {
              await _googleSignIn.signIn();
              setState(() {
                isSignedIn = true;
              });
            } catch (e) {
              print("Error signing in: $e");
            }
          },
          child: Text("Login with Google"),
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late GoogleMapController mapController;
  String searchInput = "";
  LatLng? currentLocation;

  @override
  void initState() {
    super.initState();
    _getLocation();
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

    // Send location to backend
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/location'),
      body: {
        'latitude': position.latitude.toString(),
        'longitude': position.longitude.toString(),
      },
    );
    print("Backend response: ${response.body}");
  }

  void _onSearch() async {
    // Send search input to backend
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/search'),
      body: {'query': searchInput},
    );
    print("Search response: ${response.body}");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Home Screen")),
      body: Column(
        children: [
          TextField(
            decoration: InputDecoration(
              labelText: "Search",
              border: OutlineInputBorder(),
            ),
            onChanged: (value) {
              searchInput = value;
            },
          ),
          ElevatedButton(onPressed: _onSearch, child: Text("Submit Search")),
          Expanded(
            child: currentLocation == null
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
            ),
          ),
        ],
      ),
    );
  }
}


import 'package:flutter/material.dart';

import 'package:google_sign_in/google_sign_in.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert'; // Add this line

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email'],
    clientId: '807837243380-ku6eat428jbumbo5dkovndj7lp3h9t8f.apps.googleusercontent.com',
  );
  bool isSignedIn = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Google OAuth Login")),
      body: Center(
        child: isSignedIn
            ? HomeScreen()
            : ElevatedButton(
          onPressed: () async {
            try {
              await _googleSignIn.signIn();
              setState(() {
                isSignedIn = true;
              });
            } catch (e) {
              print("Error signing in: $e");
            }
          },
          child: Text("Login with Google"),
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late GoogleMapController mapController;
  String searchInput = "";
  LatLng? currentLocation;
  String userResponse = ""; // To store the response from the backend
  final String userId = "123"; // Replace with actual user ID

  @override
  void initState() {
    super.initState();
    _getLocation();
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

    // Send location to backend
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/location'),
      body: {
        'latitude': position.latitude.toString(),
        'longitude': position.longitude.toString(),
      },
    );
    print("Backend response: ${response.body}");
  }

  void _onSearch() async {
    // Send search input to backend
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/search'),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {
        'user_id': userId,
        'query': searchInput,
      },
    );

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      setState(() {
        userResponse = responseData['response']; // Update the UI with the response
      });
    } else {
      setState(() {
        userResponse = "Error: ${response.statusCode}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("SOLEMLU!")),
      body: Stack(
        children: [
          currentLocation == null
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
          ),
          Positioned(
            top: 20,
            left: 20,
            right: 20,
            child: Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        decoration: InputDecoration(
                          labelText: "Search",
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (value) {
                          setState(() {
                            searchInput = value;
                          });
                        },
                      ),
                    ),
                    SizedBox(width: 10),
                    ElevatedButton(
                      onPressed: _onSearch,
                      child: Text("Search"),
                    ),
                  ],
                ),
              ),
            ),
          ),
          if (userResponse.isNotEmpty)
            Positioned(
              bottom: 20,
              left: 20,
              right: 20,
              child: Card(
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(userResponse),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

*/
import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email'],
    clientId: '807837243380-ku6eat428jbumbo5dkovndj7lp3h9t8f.apps.googleusercontent.com',
  );
  bool isSignedIn = false;

  Future<void> _handleSignIn() async {
    try {
      await _googleSignIn.signIn();
      setState(() {
        isSignedIn = true;
      });
    } catch (error) {
      print("Error signing in: $error");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Google OAuth Login")),
      body: Center(
        child: isSignedIn
            ? HomeScreen()
            : Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("Sign in with Google"),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _handleSignIn,
              child: Text("Sign in with Google"),
            ),
          ],
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late GoogleMapController mapController;
  String searchInput = "";
  LatLng? currentLocation;
  String userResponse = "";
  final String userId = "123"; // Replace with actual user ID

  @override
  void initState() {
    super.initState();
    _getLocation();
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

    // Send location to backend
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/location'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        'latitude': position.latitude,
        'longitude': position.longitude,
      }),
    );

    print("Backend response: ${response.body}");
  }

  void _onSearch() async {
    // Send search input to backend
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/search'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        'user_id': userId,
        'query': searchInput,
      }),
    );



    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      setState(() {
        userResponse = responseData['response'];
      });
    } else {
      setState(() {
        userResponse = "Error: ${response.statusCode}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("SOLEMLU!")),
      body: Stack(
        children: [
          currentLocation == null
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
          ),
          Positioned(
            top: 20,
            left: 20,
            right: 20,
            child: Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        decoration: InputDecoration(
                          labelText: "Search",
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (value) {
                          setState(() {
                            searchInput = value;
                          });
                        },
                      ),
                    ),
                    SizedBox(width: 10),
                    ElevatedButton(
                      onPressed: _onSearch,
                      child: Text("Search"),
                    ),
                  ],
                ),
              ),
            ),
          ),
          if (userResponse.isNotEmpty)
            Positioned(
              bottom: 20,
              left: 20,
              right: 20,
              child: Card(
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(userResponse),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

