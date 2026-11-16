<script setup>
defineProps({
  message: { type: String, default: '' },
  error: { type: String, default: '' },
  loading: { type: Boolean, default: false },
})
</script>

<template>
  <div class="result-panel">
    <div class="result-top"><span>TU SALUDO</span><span>{{ loading ? 'Cargando' : error ? 'Error' : message ? 'Completado' : 'En espera' }}</span></div>
    <div class="result-content" :class="{ loading, error: !!error, success: !!message }" role="status" aria-live="polite" aria-atomic="true">
      <span class="state-icon" aria-hidden="true">{{ loading ? '' : error ? '!' : message ? '✓' : '→' }}</span>
      <template v-if="loading"><h2>Preparando tu saludo…</h2><p>Un momento, estamos en ello.</p></template>
      <template v-else-if="error"><h2>No se ha podido conectar</h2><p>{{ error }}</p></template>
      <template v-else-if="message"><h2>{{ message }}</h2><p>Tu saludo está listo.</p></template>
      <template v-else><h2>Tu saludo empieza aquí.</h2><p>Cuando pulses Saludar, aparecerá en este espacio.</p></template>
    </div>
    <p class="result-bottom">Algo sencillo, hecho para ti.</p>
  </div>
</template>
