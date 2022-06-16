import { HttpErrorResponse } from '@angular/common/http';
import { NgForm } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { ApplicationService } from 'src/app/Services/application.service';
import { Router } from '@angular/router';
import { Tweet } from 'src/app/Models/Tweet';
import { Result } from 'src/app/Models/Result';

@Component({
  selector: 'app-tweetpolarity',
  templateUrl: './tweetpolarity.component.html',
  styleUrls: ['./tweetpolarity.component.css']
})
export class TweetpolarityComponent implements OnInit {

  public req : Tweet= new Tweet();
  public hidePage = false;

  constructor(private router: Router, private applicationService : ApplicationService) { }

  ngOnInit(): void {
  }

  onClickSubmit(data) {
     console.log("Entered Email id : " + data.txt);
   }


   public GetPolarity(requestForm : NgForm){
    console.log(this.req);
    this.applicationService.GetPolarity(this.req).subscribe(
      (response: Result[]) => {
        this.applicationService.setResults(response);
        if(response[0].value==1)
          console.log("Positif");
        else
        console.log("Negatif");
      },
      (error: HttpErrorResponse) => {
        alert(error.message);
        requestForm.reset();
      }
    );
  }

}
