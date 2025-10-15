<template>
    <div >
        <NavBar></NavBar>
        <h2>Welcome {{ username }} to admin dashboard</h2>
        <Parkinglot></Parkinglot>
        <router-view></router-view>
        
    </div>

</template>
<script>
import NavBar from '../components/navbar.vue';
import Parkinglot from '../components/parking_lot.vue';
export default ({
    name: "LoginComp",
    data() {
        return {
            
            username:"",
            userrole:""
        }
    },
    mounted(){
    },
    components:{
        NavBar,
        Parkinglot
    }

})

</script>