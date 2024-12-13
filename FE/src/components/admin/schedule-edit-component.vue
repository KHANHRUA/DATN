<template>
  <div>
    <el-dialog v-model="modal" :show-close="false" class="modal-container"
               style="width: 60%;min-width:400px;height: fit-content;">
      <template v-slot:header>
        <div class="header-modal">
          Create schedule
        </div>
      </template>
      <template v-slot:default>
        <div>
          <el-row :gutter="20" align="middle" class="table-header" justify="space-between">
            <el-col :span="6">
              <el-button class="button" size="small" type="primary" @click="changeWeek('previous')">Previous</el-button>
            </el-col>
            <el-col :span="6">
              <el-select v-model="form.class" :remote-method="fetchClasses" filterable placeholder="Class" remote
                         remote-show-suffix @change="getClassObject">
                <el-option v-for="item in classList" :key="item.id" :label="item.class_name" :value="item.id"/>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-date-picker
                  @change="changeWeek"
                  v-model="form.week"
                  format="[Week] ww"
                  placeholder="Pick a week"
                  type="week"
              />
            </el-col>
            <el-col :span="6" style="display: flex;justify-content: end">
              <el-button class="button" size="small" type="primary" @click="changeWeek('next')">Next</el-button>
            </el-col>
          </el-row>

          <el-table :data="timeTable" border style="width: 100%" @cell-dblclick="selectDate">
            <!-- Cột Tiết -->
            <el-table-column align="center" label="Session" prop="period" width="140">
              <template #default="scope">
                <div class="period-cell">{{ scope.row.period }}</div>
              </template>
            </el-table-column>

            <!-- Cột Thứ -->
            <el-table-column v-for="day in days" :key="day.index" :label="day.value" align="center" min-width="120">
              <template #default="scope">
                <div v-if="scope.row" :class="scope.row[day.value] ? 'subject-cell' : {}">{{ scope.row[day.value] }}
                </div>
              </template>
            </el-table-column>

            <!-- Cột Giờ -->
            <el-table-column align="center" label="Time start" prop="time" width="100">
              <template #default="scope">
                <div class="time-cell">{{
                    scope.row.time < 10 ? `0${scope.row.time} : 00` : `${scope.row.time} : 00`
                  }}
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
      <template v-slot:footer>
        <div style="display: flex;justify-content: space-between">
          <div>
            <el-button type="success" @click="openCreateSchedule">Create new</el-button>
          </div>
          <div>
            <el-button @click="hide">Cancel</el-button>
            <el-button type="primary">Confirm</el-button>
          </div>
        </div>
      </template>
    </el-dialog>
    <create-schedule v-if="classObject" ref="createSchedule" :class-picked="classObject" @create-session="fetchSession"/>
  </div>
</template>

<script>

import {debounce} from "lodash";
import ClassService from "@/service/class-api/api.ts";
import CreateSchedule from "@/components/common/create-schedule.vue";
import SessionService from "@/service/session-api/api.ts";

export default {
  name: 'ScheduleEditComponent',
  components: {CreateSchedule},
  data() {
    return {
      modal: false,
      classObject: null,
      days: [
        {
          index: 0,
          value: 'Monday'
        },
        {
          index: 1,
          value: 'Tuesday',
        },
        {
          index: 2,
          value: 'Wednesday'
        },
        {
          index: 3,
          value: 'Thursday'
        }, {
          index: 4,
          value: 'Friday'
        }, {
          index: 5,
          value: 'Saturday'
        }, {
          index: 6,
          value: 'Sunday'
        }
      ],
      roomList: [],
      timeTable: [
        {
          period: "Class period 1",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 7
        },
        {
          period: "Class period 3",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 9
        },
        {
          period: "Class period 5",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 11
        },
        {
          period: "Class period 7",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 14
        },
        {
          period: "Class period 9",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 16
        },
        {
          period: "Class period 11",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 18
        },
      ],
      form: {
        class: null,
        week: null,
        endWeek: null
      },
      classList: [],
      loading: {
        class: false,
        user: false
      },
      classDebounce: null,
      setDefaultWeek() {
        const today = new Date();
        const dayOfWeek = today.getDay();
        const difference = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

        // Tính ngày Thứ 2 đầu tuần
        const monday = new Date(today);
        monday.setDate(today.getDate() - difference);
        monday.setHours(0, 0, 0, 0);

        // Lấy ngày Thứ 7 tuần đó
        const saturday = new Date(monday);
        saturday.setDate(monday.getDate() + 6); // Thêm 6 ngày để tới Thứ 7
        // Gán Thứ 2 và Thứ 7 vào form
        this.form.week = monday;   // Thứ 2
        this.form.endWeek = saturday;  // Thứ 7
        // console.log(new Date(this.form.week).getTime())
      },
    }
  },
  created() {
    this.fetchClasses();
    this.setDefaultWeek();
  },
  methods: {
    show() {
      this.setDefaultWeek();
      this.modal = true
    },

    hide() {
      this.form = {
        week: null,
        class: null,
        user: null,
        endWeek: null
      }
      this.classObject = null
      this.modal = false
    },

    getDayOfWeek(timestamp) {
      const daysOfWeek = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ];
      const date = new Date(timestamp);
      return daysOfWeek[date.getDay()];
    },

    fetchSession() {
      if (this.form.class) {
        const query = {
          class_id: this.form.class,
          date_from: this.form.week.getTime(),
          date_to: this.form.endWeek.getTime()
        }
        this.resetTable()
        SessionService.GetSession(query).then(data => {
          const tableTemp = this.timeTable
          data.data.map(item => {
            const day_of_week = this.getDayOfWeek(item.start_at)
            for (let i = 0; i < tableTemp.length; i++) {
              if (tableTemp[i].time === item.class_period) {
                tableTemp[i][day_of_week] = item.subject?.name;
              }
            }
          })
          this.timeTable = [...tableTemp]
        }).catch(error => {
          console.log(error)
        })
      }
    },

    fetchClasses(filter) {
      this.classDebounce?.cancel()
      this.classDebounce = debounce(() => {
            this.loading.class = true
            ClassService.getAllClasses(filter).then((data) => {
                  this.classList = data.data
                }
            ).catch((error) => {
                  console.log(error)
                }
            ).finally(() => {
              this.loading.class = false
            })
          }
          , 1500)()
    },

    changeWeek(buttonClick) {
      if (buttonClick === 'next') {
        const previousWeek = new Date(this.form.week);
        previousWeek.setDate(previousWeek.getDate() + 7);
        const saturday = new Date(previousWeek);
        saturday.setDate(previousWeek.getDate() + 6);
        this.form.week = previousWeek;
        this.form.endWeek = saturday;
      }
      if (buttonClick === 'previous') {
        const nextWeek = new Date(this.form.week);
        nextWeek.setDate(nextWeek.getDate() - 7);
        const saturday = new Date(nextWeek);
        saturday.setDate(nextWeek.getDate() + 6);
        this.form.week = nextWeek;
        this.form.endWeek = saturday;
      }
      this.fetchSession()
    },

    selectDate(event) {
      console.log(event.period)
    },

    openCreateSchedule() {
      if (!this.classObject) {
        this.$message({
          message: "Please choose an class first",
          type: 'warning'
        })
      } else {
        this.$refs.createSchedule.show()
      }
    },

    getClassObject(classPicked) {
      this.classObject = this.classList.find(item => item.id === classPicked)
      this.fetchSession()
    },

    resetTable() {
      this.timeTable = [
        {
          period: "Class period 1",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 7
        },
        {
          period: "Class period 3",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 9
        },
        {
          period: "Class period 5",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 11
        },
        {
          period: "Class period 7",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 14
        },
        {
          period: "Class period 9",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 16
        },
        {
          period: "Class period 11",
          Monday: null,
          Tuesday: null,
          Wednesday: null,
          Thursday: null,
          Friday: null,
          Saturday: null,
          Sunday: null,
          time: 18
        },
      ]
    }
  }
}
</script>

<style scoped>
.table-header {
  margin-bottom: 10px;
}

.period-cell {
  background-color: #409eff;
  color: #fff;
  font-weight: bold;
  padding: 5px 0;
  border-radius: 5px;
}

.subject-cell {
  background-color: #c9e4ff;
  font-weight: bold;
  padding: 5px 0;
  border-radius: 5px;
  border: 1px #c7c7c7 solid;
}

.time-cell {
  background-color: #409eff;
  border-radius: 5px;
  color: #fff;
  padding: 5px 0;
  font-weight: bold;
}

.button {
  height: 30px;
  width: 80px;
}
</style>