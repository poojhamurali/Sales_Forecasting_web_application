import { Component } from '@angular/core';
import { HttpClient, HttpHeaders,HttpParams} from '@angular/common/http';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  fileupload: File | undefined;
  jsonData: any;
  number: number =0;
  selected: string=" ";
  periodicity:string="";

  dashboard(){
  }
  constructor(private http:HttpClient){}

  onFileSelected(event: any){
    
    if (event.target.files.length>0) {
      const file = event.target.files[0];
      this.fileupload=file;
      
    }
  }
  onsubmit(){
  if(this.fileupload){
    const formData: FormData = new FormData();
    formData.append('file',this.fileupload,this.fileupload.name,);
    formData.append('number',this.number.toString());
    formData.append('selected',this.selected);
    formData.append('periodicity',this.periodicity)

    this.http.post('http://localhost:5000/api/file_upload',formData).subscribe(
      (res)=>{
        this.jsonData=res;
        console.log(this.jsonData.data);
      }
    );
  
  
  }
}
   
}


