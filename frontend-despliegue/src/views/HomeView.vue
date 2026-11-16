<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="home-layout" aria-labelledby="home-title">
    <div>
      <p class="eyebrow">Iron Gym · Bienvenido</p>
      <h1 id="home-title">Todo empieza<br>con un hello.</h1>
      <p class="intro">Un espacio sencillo para empezar. Escribe tu nombre, recibe un saludo y sigue adelante.</p>
      <RouterLink class="primary" to="/hello">Ir al saludo <span class="arrow" aria-hidden="true">→</span></RouterLink>
    </div>
    <div class="home-art" aria-hidden="true">
      <span>01 / Una primera conexión</span>
      <span class="hello-type">Hello<br>World_</span>
      <span>Un nombre. Un saludo. Así de fácil.</span>
    </div>
  </section>
</template>
