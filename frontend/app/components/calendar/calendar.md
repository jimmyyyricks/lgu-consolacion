# QCalendarMonth API

## Style

day-style
: (timestamp) => Array | Object | String
Description
Gets called to provide custom styling of a day
day-class
: (timestamp) => Array | Object | String
Description
Gets called to provide custom styling (via classes) of a day
weekday-style
: (data) => Object
Description
Gets called to provide custom styling of a weekday
weekday-class
: (data) => Object
Description
Gets called to provide custom styling (via classes) of a weekday
day-padding
: String
Description
Overrides the padding to be used for a day element. You can use any CSS padding format
short-month-label
: Boolean
Description
Makes the month label short. January becomes Jan...
hover
: Boolean
Description
Changes the style selected-start-end-dates selection when in mini-mode. Typically, set this to true on mousedown and false on mouseup
month-label-size
: String
Description
This property is used change the size of the month label button. This property is ignored when mini-mode is set to true
date-type
: String
Description
Shows the current date button as either a circle, rounded or a square
weekday-align
: String
Description
Determines the weekday (ie: Sunday, Monday, etc) alignment
date-align
: String
Description
Determines the date (ie: 2, 3, etc) alignment
bordered
: Boolean
Description
Places a border around the calendar
dark
: Boolean
Description
Places the calendar into dark mode
no-scroll
: Boolean
Description
Turns off the internal scrollbar. Useful if you want to handle your own scrolling
date-header
: String
Description
Determines how the date header will be displayed

## model

now
: String
Description
This is the currently displayed date (highlighted). If not set, then the current date is used
min-weeks
: Number | String
Description
The minimum number of weeks to be displayed
max-days
: Number
Description
The number of days to be displayed. Do not use with week or month views (set to 0 if setting the view dynamically)
model-value
: String
Description
Model of the component; Either use this property (along with a listener for 'update:model-value' event) OR use v-model directive. When set as YYYY-MM-DD, the calendar will display the current view on this date. If empty, then it will be changed to the current date which will be emitted
weekdays
: Array
Description
The normal weekdays array looks like this [0,1,2,3,4,5,6] where 0=Sunday, 1=Monday, etc. A week that starts on Monday, would look like this: [1,2,3,4,5,6,0] and a 5-day workweek would look like this: [1,2,3,4,5]
locale
: String
Description
Used to change the locale of the calendar. Any acceptable locale can be used that is recognized by the browser. If the locale fails, then 'en-US' is the fallback
disabled-days
: Array
Description
An array of string dates in the form YYYY-MM-DD that will be disabled. If an array is contained within the array with a start and end date, it will be treated as a range
disabled-before
: String
Description
A date in the form YYYY-MM-DD where all dates before, and including, will be disabled
disabled-after
: String
Description
A date in the form YYYY-MM-DD where all dates after, and including, will be disabled
selected-dates
: Array | Set
Description
An array of string dates in the form YYYY-MM-DD that will be selected. Interval-based calendars use YYYY-MM-DD HH:mm

## content

show-work-weeks
: Boolean
Description
Show work weeks
show-month-label
: Boolean
Description
Shows the month label - this occurs on the 1st of the month
show-day-of-year-label
: Boolean
Description
Show the day of the year - this occurs in the top right of each day element. If show-month-label is true, then that day is skipped
short-weekday-label
: Boolean
Description
Displays the weekday label in short format. For instance, 'Monday' would become 'Mon'
no-header
: Boolean
Description
Do not display the header
no-default-header-text
: Boolean
Description
Do not display the weekday text in the header
no-default-header-btn
: Boolean
Description
Do not display the date button in the header

## behavior

use-navigation
: Boolean
Description
Allows keyboard navigation
day-height
: Number | String
Description
The maximum height in pixels for the day height. Using 0 will make the rows variable height based on content.
day-min-height
: Number | String
Description
The minimum height to be used
enable-outside-days
: Boolean
Description
By default, outside days are disabled in month view. Use the property to enable them.
no-outside-days
: Boolean
Description
Do not display the labels of outside days
mini-mode
: Boolean | String
Description
When true puts the calendar into mini-mode. When auto, then the property breakpoint is used to determine when the calendar will be put into mini-mode
breakpoint
: String | Number
Description
This property is used when mini-mode is set with auto
no-aria
: Boolean
Description
Turns off automatical generation of aria labels for timestamps
no-active-date
: Boolean
Description
This controls whether the q-active-date css class is set when a user clicks on a date label (button)
min-weekday-label
: Number | String
Description
The minimal number of weekday characters when truncation occurs
weekday-breakpoints
: Array
Description
The breakpoint widths where weekday truncation occurs (needs 2 values)
animated
: Boolean
Description
Turns on animated transitions
transition-prev
: String
Description
When animated property is true, transition to use for previous calendar display
transition-next
: String
Description
When animated property is true, transition to use for next calendar display
disabled-weekdays
: Array
Description
Similar to weekdays property, except values included in this array are automatically made disabled
drag-enter-func
: (event, type, data) => Boolean
Description
The function to handle dragenter events
drag-over-func
: (event, type, data) => Boolean
Description
The function to handle dragover events. You must call in your e.preventDefault() for Drag and Drop to work properly
drag-leave-func
: (event, type, data) => Boolean
Description
The function to handle dragleave events
drop-func
: (event, type, data) => Boolean
Description
The function to handle drop events
selected-start-end-dates
: Array
Description
An array of two dates in format YYYY-MM-DD for selection purposes. Interval-based calendars use YYYY-MM-DD HH:mm
hoverable
: Boolean
Description
Allows certain cells within the calendar to be hovered
focusable
: Boolean
Description
Allows certain cells within the calendar to receive focus
focus-type
: Array
Description
Describes what can become focusable
cell-width
: String | Number
Description
Sets day cell width and turns on sticky mode. Width must be css measurement if a string, otherwise it's in pixels

---

from Documentaion

<template>
  <div class="subcontent">
    <navigation-bar @today="onToday" @prev="onPrev" @next="onNext" />

    <div class="row no-wrap" style="width: 600px">
      <span class="col-shrink no-wrap" style="min-width: 142px">Day Height:</span>
      <q-slider
        v-model="dayHeight"
        :min="0"
        :max="200"
        label
        label-always
        :label-value="dayHeight + 'px'"
        class="col"
      />
    </div>

    <div class="row no-wrap" style="width: 600px">
      <span class="col-shrink no-wrap" style="min-width: 142px">Day Min. Height:</span>
      <q-slider
        v-model="dayMinHeight"
        :min="0"
        :max="200"
        label
        label-always
        :label-value="dayMinHeight + 'px'"
        class="col"
      />
    </div>

    <div class="row justify-center">
      <div :style="calendarStyle">
        <q-calendar-month
          ref="calendar"
          v-model="selectedDate"
          :day-height="dayHeight"
          :day-min-height="dayMinHeight"
          animated
          bordered
          @change="onChange"
          @moved="onMoved"
          @click-date="onClickDate"
          @click-day="onClickDay"
          @click-workweek="onClickWorkweek"
          @click-head-workweek="onClickHeadWorkweek"
          @click-head-day="onClickHeadDay"
        />
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { QCalendarMonth, today, Timestamp } from '@quasar/quasar-ui-qcalendar'
import '@quasar/quasar-ui-qcalendar/index.css'

import { ref, computed, type CSSProperties } from 'vue'
import NavigationBar from 'components/NavigationBar.vue'

const calendar = ref<QCalendarMonth>(),
  selectedDate = ref(today()),
  dayHeight = ref(50),
  dayMinHeight = ref(50)

const calendarStyle = computed<CSSProperties>(() => {
  return {
    display: 'flex',
    maxWidth: '800px',
    width: '100%',
    height: dayHeight.value === 0 && dayMinHeight.value === 0 ? '600px' : '',
  }
})

function onToday() {
  if (calendar.value) {
    calendar.value.moveToToday()
  }
}
function onPrev() {
  if (calendar.value) {
    calendar.value.prev()
  }
}
function onNext() {
  if (calendar.value) {
    calendar.value.next()
  }
}
function onMoved(data: Timestamp) {
  console.info('onMoved', data)
}
function onChange(data: { start: Timestamp; end: Timestamp; days: Timestamp[] }) {
  console.info('onChange', data)
}
function onClickDate(data: Timestamp) {
  console.info('onClickDate', data)
}
function onClickDay(data: Timestamp) {
  console.info('onClickDay', data)
}
function onClickWorkweek(data: Timestamp) {
  console.info('onClickWorkweek', data)
}
function onClickHeadDay(data: Timestamp) {
  console.info('onClickHeadDay', data)
}
function onClickHeadWorkweek(data: Timestamp) {
  console.info('onClickHeadWorkweek', data)
}
</script>
