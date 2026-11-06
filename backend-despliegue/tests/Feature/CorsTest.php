<?php

namespace Tests\Feature;

use PHPUnit\Framework\Attributes\TestWith;
use Tests\TestCase;

class CorsTest extends TestCase
{
    #[TestWith(['http://localhost:5173'])]
    #[TestWith(['http://127.0.0.1:5173'])]
    public function test_allows_the_frontend_origin(string $origin): void
    {
        $this->withHeader('Origin', $origin)->getJson('/api/hello')
            ->assertOk()
            ->assertHeader('Access-Control-Allow-Origin', $origin);
    }

    public function test_omits_cors_permission_for_an_untrusted_origin(): void
    {
        $this->withHeader('Origin', 'http://web-maliciosa.com')->getJson('/api/hello')
            ->assertOk()
            ->assertHeaderMissing('Access-Control-Allow-Origin');
    }

    public function test_returns_204_for_an_allowed_preflight(): void
    {
        $this->withHeaders([
            'Origin' => 'http://localhost:5173',
            'Access-Control-Request-Method' => 'GET',
            'Access-Control-Request-Headers' => 'X-Requested-With',
        ])->options('/api/hello')
            ->assertNoContent()
            ->assertHeader('Access-Control-Allow-Origin', 'http://localhost:5173')
            ->assertHeader('Access-Control-Allow-Methods', 'GET')
            ->assertHeader('Access-Control-Allow-Headers', 'x-requested-with');
    }
}
