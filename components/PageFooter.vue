<template>
  <div class="footer">
    <NuxtLink href="/" draggable="false" :class="{ active: isRouteActive('/') }">Home</NuxtLink>
    <NuxtLink href="/about" draggable="false" :class="{ active: isRouteActive('/about') }">About</NuxtLink>
    <NuxtLink href="/faq" draggable="false" :class="{ active: isRouteActive('/faq') }">FAQ</NuxtLink>
    <NuxtLink href="#" draggable="false" class="right-aligned-button" @click.prevent="toggleDashboard" :class="{ active: isDashboardLoginPanelActive }">Dashboard</NuxtLink>
    <div class="dashboard-login-board" :class="{ active: isDashboardLoginPanelActive }">
      <div>
        <input placeholder="Access Key" type="password" :disabled="isAuthContentDisabled" v-show="!isAuthContentHidden">
        <button v-show="!isAuthContentHidden" :disabled="isAuthContentDisabled" @click="tryLogin">Auth</button>
        <p v-show="isAuthContentHidden">{{ authErrorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const isDashboardLoginPanelActive = ref(false)
const isAuthContentDisabled = ref(false)

const toggleDashboard = () => {
  isDashboardLoginPanelActive.value = !isDashboardLoginPanelActive.value
}

const route = useRoute()

const isRouteActive = (path: string) => {
  return route.path === path && !isDashboardLoginPanelActive.value
}

const isAuthContentHidden = ref(false)
const authErrorMessage = ref('')

const tryLogin = async () =>
{
  isAuthContentDisabled.value = true;
}

function setLoginError(errorMessage)
{
  isAuthContentHidden.value = true
  authErrorMessage.value = errorMessage

  setTimeout(() => {
    authErrorMessage.value = ""
    isAuthContentHidden.value = false
  }, 2222);
}
</script>

<style>

</style>