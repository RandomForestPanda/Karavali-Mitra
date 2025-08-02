import 'package:google_sign_in/google_sign_in.dart';

class AuthService {
  final GoogleSignIn _googleSignIn = GoogleSignIn();

  Future<void> signInWithGoogle() async {
    try {
      await _googleSignIn.signIn();
      // User signed in
      print('User signed in: ${_googleSignIn.currentUser}');
    } catch (error) {
      print('Sign in failed: $error');
    }
  }

  Future<void> signOut() async {
    await _googleSignIn.signOut();
    print('User signed out');
  }
}
