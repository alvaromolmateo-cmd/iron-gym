<script setup>
import { nextTick } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'

useRouter().afterEach(async () => {
  await nextTick()
  document.querySelector('#main')?.focus({ preventScroll: true })
})
</script>

<template>
  <a class="skip" href="#main">Saltar al contenido</a>
  <header>
    <div class="header-inner">
      <RouterLink class="brand" to="/" aria-label="Iron Gym, inicio">
        <span class="mark" aria-hidden="true"><i></i><i></i><i></i></span>
        <span>Iron <strong>Gym</strong></span>
      </RouterLink>
      <nav aria-label="Navegación principal">
        <RouterLink to="/">Inicio</RouterLink><RouterLink to="/hello">Hello</RouterLink>
      </nav>
      <span class="header-note">Una pequeña interacción. Un buen comienzo.</span>
    </div>
  </header>
  <main id="main" tabindex="-1">
    <RouterView />
    <footer><span>Iron Gym · Frontend 02</span><span>Un nombre. Un saludo. Así de fácil.</span></footer>
  </main>
</template>
