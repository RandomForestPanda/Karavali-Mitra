# Google Maps and Play Services rules
-keep class com.google.android.gms.** { *; }
-dontwarn com.google.android.gms.**

# Geolocator plugin
-keep class io.flutter.plugins.geolocator.** { *; }
-dontwarn io.flutter.plugins.geolocator.**
