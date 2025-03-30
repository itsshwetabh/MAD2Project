

<template>
    <div style="display:flex;" >
      <LandingLeft/>
      <LandingRight/>
    </div>
    
  </template>
  
  <script>
  import LandingLeft from '../Landing/LandingLeft.vue';
  import LandingRight from '../Landing/LandingRight.vue';
  export default{
    name: 'App',
    components: {
      LandingLeft,
      LandingRight,
    },
    mounted(){
      if(localStorage.getItem('userData'))
    {
      const role = JSON.parse(localStorage.getItem('userData')).role
      if(role=='user')
      {
        this.$router.push('/UserDashboard')
      }
      else
      {
        this.$router.push('/AdminDashboard')
      }
    }
    }
  }
  </script>
  
  
  