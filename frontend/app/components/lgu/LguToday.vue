<script setup lang="ts">
interface WeatherResponse {
  current: {
    temperature_2m: number
    relative_humidity_2m: number
    apparent_temperature: number
    weather_code: number
    wind_speed_10m: number
  }
  daily: {
    temperature_2m_max: number[]
    temperature_2m_min: number[]
  }
}

const municipalHall = {
  latitude: 10.37583,
  longitude: 123.957206
}

const { data: weather, error, pending } = await useFetch<WeatherResponse>(
  'https://api.open-meteo.com/v1/forecast',
  {
    query: {
      ...municipalHall,
      current: 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m',
      daily: 'temperature_2m_max,temperature_2m_min',
      timezone: 'Asia/Manila',
      forecast_days: 1
    },
    timeout: 8000
  }
)

const weatherCodeLabels: Record<number, string> = {
  0: 'Clear sky',
  1: 'Mostly clear',
  2: 'Partly cloudy',
  3: 'Overcast',
  45: 'Fog',
  48: 'Freezing fog',
  51: 'Light drizzle',
  53: 'Drizzle',
  55: 'Heavy drizzle',
  56: 'Freezing drizzle',
  57: 'Heavy freezing drizzle',
  61: 'Light rain',
  63: 'Rain',
  65: 'Heavy rain',
  66: 'Freezing rain',
  67: 'Heavy freezing rain',
  71: 'Light snow',
  73: 'Snow',
  75: 'Heavy snow',
  77: 'Snow grains',
  80: 'Rain showers',
  81: 'Rain showers',
  82: 'Heavy rain showers',
  85: 'Snow showers',
  86: 'Heavy snow showers',
  95: 'Thunderstorm',
  96: 'Thunderstorm with hail',
  99: 'Heavy thunderstorm with hail'
}

const weatherCondition = computed(() => {
  const code = weather.value?.current.weather_code
  return code === undefined ? '' : weatherCodeLabels[code] ?? 'Variable conditions'
})

const municipalHallMapUrl = `https://maps.google.com/maps?q=${municipalHall.latitude}%2C${municipalHall.longitude}&z=16&output=embed`
</script>

<template>
  <UPageSection
    id="today"
    title="Consolacion at a Glance"
    description="Current local weather and places to explore."
    aria-label="Consolacion at a Glance"
    class="bg-primary-50 dark:bg-primary-950/40"
    :ui="{
      container: 'gap-7 py-12 sm:gap-8 sm:py-14 lg:py-16',
      title: 'text-left font-domine text-3xl font-semibold leading-tight tracking-normal sm:text-4xl',
      description: 'mt-3 text-left text-base leading-7 text-toned'
    }"
  >
    <div class="grid gap-8 lg:grid-cols-2 lg:gap-10">
      <UCard
        variant="outline"
        aria-label="Current Weather in Consolacion"
        :ui="{ root: 'h-full overflow-hidden', body: 'p-0!' }"
      >
        <iframe
          :src="municipalHallMapUrl"
          title="Map of the Consolacion Government Center, Cebu"
          class="block h-48 w-full border-0 sm:h-56"
          loading="lazy"
          allowfullscreen
          referrerpolicy="no-referrer-when-downgrade"
        />
        <div
          role="group"
          aria-label="Current Weather Conditions"
          class="p-5 sm:p-6"
        >
          <USkeleton
            v-if="pending"
            class="h-28 w-full"
          />
          <UAlert
            v-else-if="error || !weather"
            color="neutral"
            variant="subtle"
            title="Current Weather Is Temporarily Unavailable"
          />
          <div v-else>
            <div class="flex items-center justify-between gap-4">
              <div>
                <p class="font-domine text-5xl font-semibold leading-none text-highlighted">
                  {{ Math.round(weather.current.temperature_2m) }}°C
                </p>
                <p class="mt-2 text-lg font-medium text-toned">
                  {{ weatherCondition }}
                </p>
              </div>
              <div class="text-right">
                <p class="text-sm text-muted">
                  Feels Like
                </p>
                <p class="mt-1 text-lg font-medium text-highlighted">
                  {{ Math.round(weather.current.apparent_temperature) }}°C
                </p>
              </div>
            </div>
            <dl class="mt-5 grid grid-cols-2 gap-4 border-t border-default pt-4 sm:grid-cols-4">
              <div>
                <dt class="text-sm text-muted">
                  High
                </dt>
                <dd class="mt-1 text-lg font-medium text-highlighted">
                  {{ Math.round(weather.daily.temperature_2m_max[0] ?? 0) }}°C
                </dd>
              </div>
              <div>
                <dt class="text-sm text-muted">
                  Low
                </dt>
                <dd class="mt-1 text-lg font-medium text-highlighted">
                  {{ Math.round(weather.daily.temperature_2m_min[0] ?? 0) }}°C
                </dd>
              </div>
              <div>
                <dt class="text-sm text-muted">
                  Humidity
                </dt>
                <dd class="mt-1 text-lg font-medium text-highlighted">
                  {{ weather.current.relative_humidity_2m }}%
                </dd>
              </div>
              <div>
                <dt class="text-sm text-muted">
                  Wind
                </dt>
                <dd class="mt-1 text-lg font-medium text-highlighted">
                  {{ Math.round(weather.current.wind_speed_10m) }} km/h
                </dd>
              </div>
            </dl>
            <p class="mt-4 text-sm text-muted">
              Weather Data by
              <a
                href="https://open-meteo.com/"
                target="_blank"
                rel="noopener"
                class="underline underline-offset-2"
              >
                Open-Meteo
              </a>
            </p>
          </div>
        </div>
      </UCard>
      <LguTourismPreview />
    </div>
  </UPageSection>
</template>
