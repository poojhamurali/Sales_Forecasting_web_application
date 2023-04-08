
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{


  uname1: string='';
  pass1: string='';
  enable_button: boolean=false;
  invalidLogin: boolean=false;
  
  constructor(private http: HttpClient, private router: Router){}

   
  
  ngOnInit(): void {
 
  }
    

  login() {
    
  
   const uname=this.uname1;
   const pass=this.pass1; 
    

    const data2={
      "uname" :this.uname1,
      "pass"  :this.pass1
    }


  this.http.post<any>("http://localhost:5000/api/login",data2).subscribe(
      (Response)=>{
        if(Response.status && Response.status.statusCode==200){
          this.router.navigate(['/dashboard'])
        }
        else{
          alert("ERROR")
        }
      }
    )
    // ,{skipLocationChange: true}

  // 
  //   if (this.email && this.password) {
  //     const loginData = { email: this.email, password: this.password };
  //     this.http.post('/register-user', loginData).subscribe((response: any) => {
  //       if (response.status === 'success') {
  //         localStorage.setItem('auth_user', JSON.stringify(response.auth_user));
  //         localStorage.setItem('status', response.status);
  //         this.router.navigate(['/dashboard']);
  //       } else {
  //         this.status = response.status;
  //       }
  //     });
  // //   }
  // }
}
}


// if (!this.uname1|| !this.pass1) {
    //   this.invalidLogin=true;
    //  return;
    // }

     // nagivateToDashboard() {
    //   // Check if uname1 and pass1 are valid
    //   if (this.uname1 && this.pass1) {
    //     // Navigate to the dashboard route
    //     this.router.navigate(['/dashboard'],{skipLocationChange:true});
    //   }
    // }

     //   ngOnInit() {
  //     const authUser = JSON.parse(localStorage.getItem('auth_user'));
  //     if (!authUser) {
  //       this.router.navigate(['/login']);
  //     }
  //   }

