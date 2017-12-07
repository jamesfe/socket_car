import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { ControlStickComponent } from './components/controlstick.component';
import { ServerTrafficComponent } from './components/servertraffic.component';

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule
    ],
    declarations: [
        AppComponent,
        ControlStickComponent,
        ServerTrafficComponent
    ],
    bootstrap: [
        AppComponent
    ]
})

export class AppModule {


}
