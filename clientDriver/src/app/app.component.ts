import { Component, OnInit } from "@angular/core";

@Component({
    selector: "socketcar",
    styleUrls: [ "./app.component.scss" ],
    template: `
        <div>
        <h1>Socket Car Controller</h1>
        <controlstick></controlstick>
        </div>
    `
})

export class AppComponent implements OnInit {
    
    public constructor() {
        console.log("In app component ts");
    }
    
    public ngOnInit(): void {}
    
}