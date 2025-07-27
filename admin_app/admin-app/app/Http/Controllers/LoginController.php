<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class LoginController extends Controller
{
    private $redirectPage = '/dashboard';

    public function showLoginForm()
    {
        return view('login');
    }

    public function login(Request $request)
    {
        $username = $request->input('username');
        $password = $request->input('password');

        return redirect($this->redirectPage . '?username=' . urlencode($username));
        // return redirect('/login')->with('error', 'Invalid credentials');
    }

    public function dashboard(Request $request)
    {
        $username = $request->query('username');
        return view('dashboard', ['username' => $username]);
    }

    public function healthCheck()
    {
        return response()->json(['status' => 'ok', 'message' => 'Application is running']);
    }
}

