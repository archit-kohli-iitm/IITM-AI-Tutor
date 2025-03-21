<template>
  <div class="container-fluid bg-light vh-100 d-flex flex-column">
    <nav class="navbar navbar-light bg-warning px-3 w-100 d-flex justify-content-between">
      <div class="d-flex align-items-center">
        <img src="../assets/image.png" alt="IITM Logo" class="logo me-2" width="50" height="50"/>
        <router-link to="/home" class="btn btn-light border-dark ms-2">Back</router-link>
        
       
      </div>
      <span class="navbar-brand mb-0 h1 text-dark">Jan 2025 - Deep Learning</span>
      <button class="btn btn-light border-dark" @click="logout">Logout</button>
    </nav>

    <div class="row flex-grow-1">
      <!-- Left Sidebar -->
      <div class="col-auto bg-dark text-white d-flex flex-column align-items-center p-3 left-sidebar">
        <div class="sidebar-item">
          <img src="../assets/sidebar-modules-selected.svg" alt="Modules" width="40" height="40"/>
          <span>Modules</span>
        </div>
        <div class="sidebar-item">
          <img src="../assets/sidebar-grades-selected.svg" alt="Grades" width="40" height="40"/>
          <span>Grades</span>
        </div>
        <router-link to="/Ai_Bot" class="sidebar-item text-white text-decoration-none">
          <img src="../assets/4505323.png" alt="AI Bot" width="40" height="40"/>
          <span>AI Bot</span>
        </router-link>
        <div class="sidebar-item">
          <img src="../assets/sidebar-calc.svg" alt="Calc" width="40" height="40"/>
          <span>Calc</span>
        </div>
      </div>

      <!-- Main Sidebar -->
      <div class="col-3 bg-white d-flex flex-column p-3 border-end">
        <h5 class="text-dark mb-4 text-center">Modules</h5>
        <div v-for="(module, index) in modules" :key="index" class="mb-2">
          <button 
            class="btn w-100 text-start" 
            :class="{'btn-warning': selectedModule === module, 'btn-light': selectedModule !== module}"
            @click="selectModule(module)">
            {{ module }}
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="col d-flex flex-column bg-light p-4">
        <h3 class="text-dark">About the Course</h3>
        <p>⭐️⭐️⭐️⭐️⭐️ - <a href="#" class="text-primary">Submit a review</a></p>

        <h4 class="text-dark">Course Faculty</h4>
        <p>Mitesh M. Khapra<br>Department of Computer Science and Engineering, IIT Madras</p>

        <h4 class="text-dark">Instructors</h4>
        <ul>
          <li>Manojkumar Khara</li>
          <li>Karthik Thiagarajan</li>
        </ul>

        <h4 class="text-dark">Study Material</h4>
        <ul>
          <li>Deep Learning, Foundations and Concepts - Chris Bishop and Hugh Bishop</li>
          <li>Deep Learning - Ian Goodfellow, Yoshua Bengio, Aaron Courville (MIT Press, 2016)</li>
          <li>Neural Networks and Deep Learning - Charu C. Aggarwal (Springer, 2019)</li>
        </ul>
        <a href="#" class="text-primary">Click here</a> to know more about course syllabus, faculty, and contents.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      modules: [
        'Course Introduction', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Supplementary Contents'
      ],
      selectedModule: null
    };
  },
  methods: {
    selectModule(module) {
      this.selectedModule = module;
    },
    reloadPage() {
      window.location.reload();
    },
    logout(){
      localStorage.clear();
      this.$router.push({name:"HOME"})
    }
  },
  mounted(){
    let user=localStorage.getItem("user-info");
    console.log(`here`)
    console.log(user)
    if(!user){
      this.$router.push({name:"Login"})
    }
  }
};
</script>

<style scoped>
.container-fluid {
  height: 100vh;
}

.navbar {
  width: 100%;
}

.text-dark {
  font-weight: bold;
}

.btn-light:hover, .btn-warning:hover {
  background-color: #ffcc00;
}

.text-primary {
  text-decoration: none;
  font-weight: bold;
}

/* Left Sidebar Styling */
.left-sidebar {
  width: 80px;
  background-color: #3f4a63;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px 0;
}

.sidebar-item span {
  font-size: 12px;
  margin-top: 5px;
}

/* Sidebar Border */
.border-end {
  border-right: 1px solid #ddd;
}
</style>
