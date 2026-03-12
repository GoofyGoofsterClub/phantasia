<template>
  <div class="central-content">
    <div class="internal-navbar">
      <h1>Dashboard</h1>
      <div class="splitter"></div>
      <NuxtLink to="#" :class="{ active: currentInternalPage == 'overview' }">overview</NuxtLink>
      <NuxtLink to="/dashboard/uploads" :class="{ active: currentInternalPage == 'uploads' }">uploads</NuxtLink>
      <NuxtLink to="/dashboard/admin" :class="{ active: currentInternalPage == 'admin' }">admin</NuxtLink>
      <NuxtLink to="#" @click.prevent="handleLogout"><Icon name="material-symbols:logout" /></NuxtLink>
    </div>
    <div class="dashboard-page-content">
      <h2>Welcome back, {{ authStore.session?.username || 'User' }}!</h2>
      <div class="flex-block">
        <div id="upload-button" class="card" style="flex: 0 0 calc(33.333% - 0.5rem);" @click="triggerFileUpload">
          <input type="file" ref="fileInput" style="display: none" @change="handleFileUpload" />
          <button class="big-upload-button">
            <Icon name="solar:upload-broken" />
            <span class="sub-text">Upload a file</span>
          </button>
        </div>
        <div style="flex: 1;">
          <div class="just-a-block">
            <div class="card">
              <div class="header">
                <p>Your statistics</p>
                <div class="delimiter"></div>
              </div>
              <ClientOnly>
                <AreaChart
                  :data="AreaChartData"
                  :height="220"
                  :categories="categories"
                  :y-grid-line="true"
                  :x-formatter="xFormatter"
                  :x-num-ticks="4"
                  :y-num-ticks="4"
                  :curve-type="CurveType.MonotoneX"
                  :legend-position="LegendPosition.Top"
                />
              </ClientOnly>
            </div>
            </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useApiUrl } from '@/composables/useApiUrl'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const currentInternalPage = ref('overview')
const fileInput = ref<HTMLInputElement | null>(null)

console.log(authStore.session?.permissions);

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  const { apiBase } = useApiUrl()
  try {
    const isValid = await authStore.verifySession()
    if (!isValid) {
      router.push('/')
      return
    }

    const response = await $fetch(`${apiBase}/uploads/create`, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Token ${authStore.accessKey}`
      }
    })
    console.log('Upload successful:', response)
    alert('Upload successful!')
  } catch (error) {
    console.error('Upload failed:', error)
    alert('Upload failed. Check console for details.')
  } finally {
    // Reset the input value so the same file can be uploaded again if needed
    target.value = ''
  }
}

// chart
interface AreaChartItem {
  date: string
  Uploads: number
  ['Views']: number
}

const categories: Record<string, BulletLegendItemInterface> = {
  Uploads: { name: 'Uploads', color: '#332cf9' },
  Views: { name: 'Views', color: '#fb2c36' },
}

const AreaChartData: AreaChartItem[] = [
  {
    date: 'Jan 1, 1970',
    Uploads: 0,
    Views: 0,
  },
  {
    date: 'Jan 2, 1970',
    Uploads: 0,
    Views: 0,
  },
  {
    date: 'Jan 3, 1970',
    Uploads: 0,
    Views: 0,
  },
  {
    date: 'Jan 4, 1970',
    Uploads: 0,
    Views: 0,
  },
  {
    date: 'Jan 5, 1970',
    Uploads: 0,
    Views: 0,
  },
  {
    date: 'Jan 6, 1970',
    Uploads: 0,
    Views: 0,
  },
  {
    date: 'Jan 7, 1970',
    Uploads: 0,
    Views: 0,
  }
]
const xFormatter = (i: number): string | number => `${AreaChartData[i]?.date}`
const sum = (arr, key) => arr.reduce((sum, obj) => sum + obj[key], 0)
</script>

<style scoped lang="scss">
@use "@/assets/css/colors" as *;
.internal-navbar
{
  width: 100%;
  vertical-align: middle;

  h1
  {
    display: inline-block;
    vertical-align: middle;
  }

  div.splitter
  {
    display: inline-block;
    vertical-align: middle;
    width: 1px;
    height: 16px;
    background: rgba(255,255,255,0.15);
    margin: 0 16px;
  }

  a
  {
    display: inline-block;
    vertical-align: middle;
    margin: 0 4px;
    padding: 4px 8px;
    text-decoration: none;
    color: rgba(255,255,255,0.6);
    font-weight: 600;

    span
    {
      color: rgba(255,255,255,0.6);
      vertical-align: middle;
    }

    &:hover, &.active
    {
      color: $background-color;
      background-color: $highlight-color;

      span
      {
        color: $background-color;
      }
    }
  }
}

.big-upload-button
{
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  cursor: pointer;
  font-size: 32px;

  span.sub-text
  {
    display: block;
    font-size: 18px;
  }

  span
  {
    color: rgba(255,255,255,0.65);
  }

  &:hover
  {
    span
    {
      color: rgba(255,255,255,1);
    }
  }
}
</style>