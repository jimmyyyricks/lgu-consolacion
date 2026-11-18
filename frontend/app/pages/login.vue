<script setup lang="ts">
const { login } = useAuth()
const router = useRouter()

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async (user?: string, pass?: string) => {
  const loginUsername = user || username.value
  const loginPassword = pass || password.value

  if (!loginUsername || !loginPassword) {
    errorMessage.value = 'Please enter username and password'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const result = await login(loginUsername, loginPassword)
    if (result.success) {
      router.push('/admin/content')
    } else {
      errorMessage.value = result.message || 'Login failed'
    }
  } catch {
    errorMessage.value = 'An error occurred during login'
  } finally {
    isLoading.value = false
  }
}

definePageMeta({
  title: 'Login',
  layout: false
})

useSeoMeta({ robots: 'noindex, nofollow' })
</script>

<template>
  <div class="flex min-h-[80vh] items-center justify-center bg-muted/30 p-4 sm:p-6">
    <UCard class="w-full max-w-md">
      <!-- Branding Header -->
      <div class="mb-8 flex flex-col items-center text-center">
        <img
          src="/images/lacion seal.jpg"
          alt="Municipality of Consolacion seal"
          class="mb-4 size-16 rounded-full object-cover"
        >
        <h1 class="font-domine text-2xl font-semibold text-highlighted">
          Staff sign in
        </h1>
        <p class="mt-1 text-sm text-muted">
          Municipality of Consolacion
        </p>
      </div>

      <form
        class="space-y-4"
        @submit.prevent="handleLogin()"
      >
        <UFormField
          label="Username"
          size="lg"
        >
          <UInput
            v-model="username"
            type="text"
            placeholder="Enter your username"
            :disabled="isLoading"
            required
            size="lg"
            class="w-full"
          />
        </UFormField>

        <UFormField
          label="Password"
          size="lg"
        >
          <UInput
            v-model="password"
            type="password"
            placeholder="Enter your password"
            :disabled="isLoading"
            required
            size="lg"
            class="w-full"
          />
        </UFormField>

        <UAlert
          v-if="errorMessage"
          color="error"
          variant="subtle"
          :description="errorMessage"
        />

        <UButton
          type="submit"
          block
          size="lg"
          :loading="isLoading"
          class="w-full"
        >
          Sign In
        </UButton>
      </form>
    </UCard>
  </div>
</template>
