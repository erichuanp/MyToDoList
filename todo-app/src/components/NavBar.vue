<template>
  <nav>
    <router-link to="/">Home</router-link>
    <span v-if="!isLoggedIn">
      | <router-link to="/login">Please Login</router-link>
      | <router-link to="/register">Register</router-link>
    </span>
    <span v-if="isLoggedIn">
      | <router-link :to="'/profile/' + userId">{{ username }}</router-link>
      | <button @click="logout">Log Out</button>
    </span>
  </nav>
</template>

<script>
import axios from 'axios';
import { EventBus } from '@/eventBus';

export default {
  name: 'NavBar',
  data() {
    return {
      isLoggedIn: false,
      username: '',
      userId: null
    };
  },
  async created() {
    this.checkLoginStatus();
    EventBus.on('user-logged-in', this.checkLoginStatus);
    EventBus.on('user-logged-out', this.handleLogout);
  },
  methods: {
    async checkLoginStatus() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('http://127.0.0.1:5000/profile', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.username = response.data.username;
          this.userId = response.data.user_id;
          this.isLoggedIn = true;
        } catch (error) {
          console.error('Error fetching user profile:', error);
        }
      } else {
        this.isLoggedIn = false;
        this.username = '';
        this.userId = null;
      }
    },
    handleLogout() {
      this.isLoggedIn = false;
      this.username = '';
      this.userId = null;
    },
    logout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;
      this.username = '';
      this.userId = null;
      this.$router.push('/login');
    }
  },
  beforeUnmount() {
    EventBus.off('user-logged-in', this.checkLoginStatus);
    EventBus.off('user-logged-out', this.handleLogout);
  }
};
</script>

<style>
nav {
  margin-bottom: 20px;
}
nav a, nav button {
  margin-right: 10px;
}
button {
  margin-left: 10px;
}
</style>
