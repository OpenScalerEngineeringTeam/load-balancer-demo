<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-sm text-center">
        <h1 class="text-3xl font-bold text-gray-800 mb-4">Welcome, <span class="text-blue-600">{{ $username ?? 'Guest' }}</span>!</h1>
        <p class="text-gray-600 mb-6">This is your dashboard.</p>
        <a href="/login" class="inline-block bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            Logout
        </a>
    </div>
</body>
</html>
