<template>
  <div style="max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; font-family: sans-serif;">
    <h2>Новый пароль</h2>
    <form @submit.prevent="handleReset" v-if="!success">
      <div style="margin-bottom: 10px;">
        <label>Введите новый пароль:</label><br>
        <input v-model="newPassword" type="password" required style="width: 100%; padding: 8px; box-sizing: border-box;" />
      </div>
      <button type="submit" style="width: 100%; padding: 10px; background: #42b883; color: white; border: none; cursor: pointer;">Сохранить</button>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </form>
    <div v-else>
      <p style="color: green;">Пароль успешно изменен!</p>
      <router-link to="/login">Перейти ко входу</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const newPassword = ref('')
const error = ref('')
const success = ref(false)
const route = useRoute()

const handleReset = async () => {
  // Достаем токен из URL (например: ?token=eyJ...)
  const token = route.query.token 
  if (!token) {
    error.value = 'Токен отсутствует в ссылке'
    return
  }

  try {
    await axios.post('http://localhost:8000/api/auth/reset-password', {
      token: token,
      new_password: newPassword.value
    })
    success.value = true
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка сброса пароля'
  }
}
</script>