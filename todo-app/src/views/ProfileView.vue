<template>
  <div>
    <h1>Profile</h1>
    <p>UID: {{ userId }}</p>
    <p>USERNAME: {{ username }}</p>
    <button @click="showDeleteForm = true" v-if="!showDeleteForm">Delete Account</button>
    <div v-if="showDeleteForm">
      <form @submit.prevent="deleteAccount">
        <div>
          <label for="username">Username:</label>
          <input type="text" v-model="deleteUsername" id="username" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" v-model="deletePassword" id="password" required />
        </div>
        <button type="submit">Delete My Account</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '@/eventBus';

export default {
  name: 'ProfileView',
  data() {
    return {
      userId: null,
      username: '',
      showDeleteForm: false,
      deleteUsername: '',
      deletePassword: '',
      message: ''
    };
  },
  async created() {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await axios.get('http://127.0.0.1:5000/profile', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.userId = response.data.user_id;
        this.username = response.data.username;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    }
  },
  methods: {
    async deleteAccount() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.$router.push('/login');
        return;
      }

      try {
        const response = await axios.delete('http://127.0.0.1:5000/delete_account', {
          headers: {
            Authorization: `Bearer ${token}`
          },
          data: {
            username: this.deleteUsername,
            password: this.deletePassword
          }
        });

        if (response.status === 200) {
          localStorage.removeItem('token');
          EventBus.emit('user-logged-out');
          this.$router.push('/');
        } else {
          this.message = response.data.message;
        }
      } catch (error) {
        console.error('Error deleting account:', error);
        if (error.response) {
          this.message = error.response.data.message;
        } else {
          this.message = 'Unknown error';
        }
      }
    }
  }
};
</script>

<style>
button {
  margin-top: 10px;
}
form {
  margin-top: 20px;
}
</style>
