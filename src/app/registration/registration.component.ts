import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent {
  sign_uname: string='';
  sign_email :string='';
  sign_pass: string='';
  

  constructor(private http: HttpClient, private router: Router) {}

  register() {
    const sname=this.sign_uname;
    const smail=this.sign_email;
    const spass=this.sign_pass;

    const data={
      "name":sname,
      "email":smail,
      "pass":spass
    }

    this.http.post("http://localhost:5000/api/register-user",data).subscribe(
      (Response)=>{
        if(Response){
          this.router.navigate([''])
        }else{
          alert("ERROR")
        }
      }
    )

  }
}