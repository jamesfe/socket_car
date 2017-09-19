import { Component, OnInit } from "@angular/core";

@Component({
    selector: "socketcar",
    styleUrls: [ "./app.component.scss" ],
    templateUrl: "./app.component.html"
})

export class AppComponent implements OnInit {
    
    public constructor() {
        console.log("In app component ts");
    }
    
    public ngOnInit(): void {}
    
}