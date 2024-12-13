<template>
  <el-dialog v-model="modal" :show-close="false" class="modal-container"
             style="width: 60%;min-width:400px;height: fit-content;">
    <template v-slot:header>
      <div class="header-modal">
        Create schedule
      </div>
    </template>
    <template v-slot:default>
      <div>
        <el-row :gutter="20" class="table-header">

          <el-col :xs="24" :span="12">
            <label>Class</label>
            <el-input :value="classPicked['class_name']" disabled/>
          </el-col>
          <el-col :xs="24" :span="12" style="display: flex;flex-direction: column">
            <label>Type of creation</label>
            <el-radio-group v-model="form.typeAdd">
              <el-radio value="period">
                Period
              </el-radio>
              <el-radio value="exactly">
                Exactly
              </el-radio>
            </el-radio-group>
          </el-col>
          <el-col v-if="form.typeAdd === 'period'" :lg="6" :span="24" style="display: flex;flex-direction: column">
            <label>Start week</label>
            <el-date-picker
                v-model="form.week"
                format="[Week] ww"
                placeholder="Pick a week"
                type="week"
                @change="pickFirstWeek"
            />
          </el-col>
          <el-col v-if="form.typeAdd === 'period'" :lg="6" :span="24" style="display: flex;flex-direction: column">
            <label>end week</label>
            <el-date-picker
                v-model="form.endWeek"
                format="[Week] ww"
                placeholder="Pick a week"
                type="week"
                @change="pickEndWeek"
            />
          </el-col>
          <el-col v-if="form.typeAdd === 'period'" :lg="6" :span="24" style="display: flex;flex-direction: column">
            <label>Date of week</label>
            <el-select v-model="form.dateOfWeek" placeholder="Time">
              <el-option v-for="item in dateList" :key="item.value" :label="`${item.label}`" :value="item.value"/>
            </el-select>
          </el-col>
          <el-col v-if="form.typeAdd === 'exactly'" :span="24" :md="6" style="display: flex;flex-direction: column">
            <label>Day</label>
            <el-date-picker
                v-model="form.day"
                placeholder="Pick a day"
                :disabled-date="disablePastDates"
                type="date"
            />
          </el-col>

          <el-col :span="24" :md="6" style="display: flex;flex-direction: column">
            <label>Time</label>
            <el-select v-model="form.time" placeholder="Time">
              <el-option v-for="item in timeList" :key="item" :label="`${item}:00`" :value="item"/>
            </el-select>
          </el-col>
          <el-col :span="24" :md="6" style="display: flex;flex-direction: column">
            <label>Subject</label>
            <el-select v-model="form.subject" placeholder="Subject" filterable remote :remote-method="fetchSubject" remote-show-suffix>
              <el-option v-for="item in subjectList" :key="item.id" :label="item.name" :value="item.id"/>
            </el-select>
          </el-col>
          <el-col :span="24" :md="6" style="display: flex;flex-direction: column">
            <label>Teacher</label>
            <el-select v-model="form.user_id" placeholder="Teacher" filterable remote :remote-method="fetchTeacher" remote-show-suffix>
              <el-option v-for="item in teacherList" :key="item.id" :label="item.name" :value="item.id"/>
            </el-select>
          </el-col>
          <el-col :span="24" :md="6" style="display: flex;flex-direction: column">
            <label>Room</label>
            <el-select v-model="form.room_id" placeholder="Room" filterable remote :remote-method="fetchRoom" remote-show-suffix>
              <el-option v-for="item in roomList" :key="item.id" :label="item.room_name" :value="item.id"/>
            </el-select>
          </el-col>
        </el-row>

        <br/>
      </div>
    </template>
    <template v-slot:footer>
      <div>
        <el-button @click="hide">Cancel</el-button>
        <el-button type="primary" @click="createSession">Confirm</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script >

import SubjectService from "@/service/subject-api/api.ts";
import {debounce} from "lodash";
import SessionService from "@/service/session-api/api.ts";
import RoomService from "@/service/room_api/api.ts";
import UserService from "@/service/user-api/api.ts";


export default {
  name: 'CreateSchedule',
  data() {
    return {
      modal: false,
      form: {
        class_id: null,
        typeAdd: 'period',
        day: null,
        week: null,
        endWeek: null,
        time: null,
        subject: null,
        dateOfWeek: null,
        room_id: null,
        user_id: null
      },
      subjectList: [],
      roomList: [],
      teacherList: [],
      timeList: [7,9,11,14,16,18],
      dateList: [
        {
          label: 'Monday',
          value: 1,
        },
        {
          label: 'Tuesday',
          value: 2,
        },
        {
          label: 'Wednesday',
          value: 3,
        },
        {
          label: 'Thursday',
          value: 4,
        },
        {
          label: 'Friday',
          value: 5,
        },
        {
          label: 'Saturday',
          value: 6,
        }
      ],
      classList: [],
      loading: {
        user: false,
        subject: false,
        room: false,
        teacher: false
      },
      subjectDebounce: null,
      classDebounce: null,
      roomDebounce: null,
      teacherDebounce: null
    }
  },
  created() {
    this.setDefaultWeek();
    this.fetchSubject();
    this.fetchRoom();
    this.fetchTeacher();
  },
  props: {
    classPicked: {
      type: Object,
      default: () => {}
    }
  },
  methods: {
    show() {
      this.modal = true
      this.form.class_id = this.classPicked.id
      this.form.day = new Date()
      this.form.day.setHours(0, 0, 0, 0)
      this.setDefaultWeek()
    },

    hide() {
      this.form = {
        startWeek: null,
        endWeek:null,
        class: null,
        user: null,
        time: null,
        typeAdd: 'period'
      }
      this.modal = false
    },

    fetchTeacher(filter){
      const param = {
        name: filter,
        role: 'teacher'
      }
      this.teacherDebounce?.cancel()
      this.teacherDebounce = debounce(() => {
        this.loading.teacher = true
        UserService.GetUsers(param).then(data => {
          this.teacherList = data.data.data
        }).catch(error => {
          console.log(error)
        }).finally(() => {
          this.loading.teacher = false
        })
      },500)()
    },

    fetchRoom(filter) {
      const data = {
        name: filter
      }
      this.roomDebounce?.cancel()
      this.roomDebounce = debounce(() => {
            this.loading.room = true
            RoomService.getRoomList(data).then((data) => {
                  this.roomList = data.data
                }
            ).catch((error) => {
                  console.log(error)
                }
            ).finally(() => {
              this.loading.room = false
            })
          }
          , 500)()
    },

    setDefaultWeek() {
      const today = new Date();
      const firstDayOfWeek = today.getDate() - today.getDay() + 1; // Thứ 2 đầu tuần
      this.form.week = new Date(today.setDate(firstDayOfWeek));
      this.form.endWeek = new Date(today.setDate(firstDayOfWeek));// Gán giá trị vào `v-model`
    },

    pickFirstWeek() {
      const dayPicked = new Date(this.form.week);
      const firstDayOfWeek = dayPicked.getDate() - dayPicked.getDay() + 1; // Thứ 2 đầu tuần
      this.form.week = new Date(dayPicked.setDate(firstDayOfWeek));
      console.log(this.form.week)
    },

    pickEndWeek() {
      const dayPicked = new Date(this.form.endWeek);
      const lastDayOfWeek = dayPicked.getDate() - dayPicked.getDay() + 1; // Thứ 2 đầu tuần
      this.form.endWeek = new Date(dayPicked.setDate(lastDayOfWeek));
    },

    disablePastDates(date) {
      const today = new Date();
      today.setHours(0, 0, 0, 0); // Reset giờ về 0
      return date < today; // Vô hiệu hóa các ngày trước hôm nay
    },

    createSession() {
      if(this.form.typeAdd === 'exactly'){
        const date_from = new Date(this.form.day).setHours( this.form.time, 0, 0, 0)
        const data = {
          class_id: this.form.class_id,
          subject_id: this.form.subject,
          date_from: date_from,
          class_period: this.form.time,
          room_id: this.form.room_id,
          user_id: this.form.user_id
        }
        SessionService.CreateSession(data).then(() => {
          this.$message({
            message: "Create session successful!",
            type: 'success',
            duration: 2000
          })
          this.modal = false
          this.$emit('create-session')
        }).catch(error =>{
          this.$message({
            message: "Create session failed!",
            type: 'error',
            duration: 2000
          })
          console.log(error)
        })
      } else{
        const data = {
          class_id: this.form.class_id,
          subject_id: this.form.subject,
          week: Math.floor(((this.form.endWeek - this.form.week) /  (1000 * 60 * 60 * 24))/ 7) + 1,
          date_from: this.form.week.setHours( this.form.time, 0, 0, 0)  + (1000 * 60 * 60 * 24)*(this.form.dateOfWeek-1),
          class_period: this.form.time,
          room_id: this.form.room_id,
          user_id: this.form.user_id
        }
        SessionService.CreateMultipleSession(data).then(() => {
          this.$message({
            message: "Create session successful!",
            type: 'success',
            duration: 2000
          })
          this.modal = false
          this.$emit('create-session')
        }).catch(error =>{
          this.$message({
            message: "Create session failed!",
            type: 'error',
            duration: 2000
          })
          console.log(error)
        })
      }
    },

    fetchSubject(filter){
      const query = {
        name: filter
      }
      this.subjectDebounce?.cancel()
      this.subjectDebounce = debounce(()=>{
        this.loading.subject = true
        SubjectService.GetSubject(query).then((data) =>{
              this.subjectList = data.data
            }
        ).catch((error)=>{
          console.log(error)}
        ).finally(()=>{
          this.loading.subject = false
        })
      },500)()
    },
  }
}
</script>
