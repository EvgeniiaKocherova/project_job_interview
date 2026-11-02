<template>
  <div style="max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; font-family: sans-serif;">
    <h2>Восстановление пароля</h2>
    <p style="font-size: 14px; color: #666;">Введите ваш Email, и мы отправим ссылку для сброса пароля.</p>
    <form @submit.prevent="handleSubmit">
      <div style="margin-bottom: 10px;">
        <label>Email:</label><br>
        <input v-model="email" type="email" required style="width: 100%; padding: 8px; box-sizing: border-box;" />
      </div>
      <button type="submit" style="width: 100%; padding: 10px; background: #42b883; color: white; border: none; cursor: pointer;">Отправить</button>
      <p v-if="message" style="color: green;">{{ message }}</p>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </form>
    <p style="margin-top: 10px;"><router-link to="/login">Вернуться к входу</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const message = ref('')
const error = ref('')

const handleSubmit = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/auth/forgot-password', {
      email: email.value
    })
    message.value = response.data.message
    error.value = ''
  } catch (err) {
    error.value = 'Ошибка отправки запроса'
    message.value = ''
  }
}
</script>