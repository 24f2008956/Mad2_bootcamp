<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto me-5 fs-4 mb-2 mb-lg-0">
                    <li class="nav-item me-3">
                        <a class="nav-link active" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item me-3">
                        <a class="nav-link" href="#">Link</a>
                    </li>
                    <li class="nav-item dropdown ">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            <i class="bi bi-person"></i>
                        </a>
                        <ul class="dropdown-menu  dropdown-menu-end">
                            <li><a class="dropdown-item" href="#">Logout</a></li>
                            
                        </ul>
                    </li>
                    
                </ul>
                
            </div>
        </div>
    </nav>

</template>
<script>
export default ({
    name: "NavBar",
    data() {
        return {
            role:""

        }
    },
    methods:{
        logout(){
            localStorage.removeItem("token")
            localStorage.removeItem("role")
            this.$router.push("/login")
        }
    },
    mounted(){
        this.role = localStorage.getItem("role")
    }

})

</script>