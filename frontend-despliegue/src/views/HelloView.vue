<script setup>
import { ref } from 'vue'
import { getHello } from '@/services/helloService'
import HelloResult from '@/components/HelloResult.vue'

const name = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

async function saludar() {
  if (loading.value) return
  loading.value = true
  message.value = ''
  error.value = ''
  try {
    message.value = await getHello(name.value)
  } catch {
    error.value = 'No se ha podido obtener el saludo del backend. Comprueba que está arrancado y vuelve a intentarlo.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section aria-labelledby="hello-title">
    <div class="page-heading">
      <div><p class="eyebrow">Un primer paso</p><h1 id="hello-title">Un saludo a tu manera.</h1>
        <p class="intro">A veces, empezar es tan sencillo como decir hello.<br>Prueba con tu nombre o deja que el saludo sea para todos.</p>
      </div><span class="index">01 / HELLO</span>
    </div>
    <div class="workspace">
      <form class="form-panel" :aria-busy="loading" @submit.prevent="saludar">
        <p class="section-caption">PERSONALIZA TU SALUDO</p>
        <label for="name">Nombre <span>(opcional)</span></label>
        <input id="name" v-model="name" name="name" type="text" autocomplete="given-name" aria-describedby="name-help" placeholder="Por ejemplo, Ana">
        <p id="name-help" class="helper">Si lo dejas vacío, recibirás «Hello World».</p>
        <button class="primary" type="submit" :disabled="loading">
          {{ loading ? 'Cargando…' : 'Saludar' }}<span class="arrow" aria-hidden="true">→</span>
        </button>
      </form>
      <HelloResult :message="message" :error="error" :loading="loading" />
    </div>
  </section>
</template>
