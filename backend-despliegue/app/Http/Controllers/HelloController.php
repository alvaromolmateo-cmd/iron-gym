<?php

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class HelloController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $name = trim((string) $request->query('name', ''));
        $message = $name === '' ? 'Hello World' : "Hello World {$name}";

        return response()->json(['message' => $message]);
    }
}
