<?php

namespace Tests\Feature;

use PHPUnit\Framework\Attributes\TestWith;
use Tests\TestCase;

class HelloTest extends TestCase
{
    #[TestWith(['/api/hello', 'Hello World'])]
    #[TestWith(['/api/hello?name=Ana', 'Hello World Ana'])]
    #[TestWith(['/api/hello?name=', 'Hello World'])]
    #[TestWith(['/api/hello?name=%20%20', 'Hello World'])]
    #[TestWith(['/api/hello?name=%20Ana%20', 'Hello World Ana'])]
    #[TestWith(['/api/hello?name=Ana%20Garc%C3%ADa', 'Hello World Ana García'])]
    #[TestWith(['/api/hello?name=0', 'Hello World 0'])]
    public function test_returns_the_expected_greeting(string $url, string $message): void
    {
        $this->getJson($url)
            ->assertOk()
            ->assertHeader('Content-Type', 'application/json')
            ->assertExactJson(['message' => $message]);
    }

    public function test_returns_404_without_the_api_prefix(): void
    {
        $this->getJson('/hello')->assertNotFound();
    }

    public function test_user_route_returns_401_without_authentication(): void
    {
        $this->getJson('/api/user')->assertUnauthorized();
    }
}
