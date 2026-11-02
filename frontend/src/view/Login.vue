<template>
  <div style="max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; font-family: sans-serif;">
    <h2>Вход в систему</h2>
    <form @submit.prevent="handleLogin">
      <div style="margin-bottom: 10px;">
        <label>Email:</label><br>
        <input v-model="email" type="email" required style="width: 100%; padding: 8px; box-sizing: border-box;" />
      </div>
      <div style="margin-bottom: 10px;">
        <label>Пароль:</label><br>
        <input v-model="password" type="password" required style="width: 100%; padding: 8px; box-sizing: border-box;" />
      </div>
      <button type="submit" style="width: 100%; padding: 10px; background: #42b883; color: white; border: none; cursor: pointer;">Войти</button>
      <p style="text-align: center; margin-top: 10px;">
  <router-link to="/forgot-password">Забыли пароль?</router-link>
</p>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const email = ref('test@test.com') // Подставил твои данные для быстрой проверки
const password = ref('secret123')
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/auth/login', {
      email: email.value,
      password: password.value
    })
    localStorage.setItem('token', response.data.access_token)
    router.push('/profile')
  } catch (err) {
    error.value = 'Неверный email или пароль'
  }
}
</script>