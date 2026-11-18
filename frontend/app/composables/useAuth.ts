import { useAuthStore } from '~/stores/auth'

export const useAuth = () => {
  const authStore = useAuthStore()
  const config = useRuntimeConfig()

  const authState = computed(() => ({
    user: authStore.user,
    token: authStore.token,
    refreshToken: authStore.refreshToken,
    isAuthenticated: authStore.isAuthenticated
  }))

  const login = async (username: string, password: string) => {
    try {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      const result = await $fetch<{
        access_token: string
        refresh_token: string
        user: {
          id: string
          username: string
          email?: string
          full_name?: string
          is_superuser?: boolean
          roles?: string[]
        }
      }>(`${config.public.apiUrl}/auth/login`, {
        method: 'POST',
        body: formData,
        credentials: 'include'
      })
      authStore.setAuth({
        token: result.access_token,
        refreshToken: result.refresh_token,
        user: result.user
      })
      return { success: true }
    } catch (error: unknown) {
      const detail = (error as { data?: { detail?: string } }).data?.detail
      return {
        success: false,
        message: detail || 'Login failed'
      }
    }
  }

  const logout = () => {
    authStore.logout()
    if (import.meta.client) {
      navigateTo('/login')
    }
  }

  return {
    authState,
    authStore,
    login,
    logout
  }
}
