import { Component, OnInit } from '@angular/core';
import { SensorsService } from 'src/app/sensors.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  constructor(private readonly sensors: SensorsService){}

  ngOnInit(): void {

    console.log("init")
    this.getSensorValues()
  }

  public async getSensorValues() {

    console.log("get sensor values")
    const values = await this.sensors.getSensorValues();
  }

}
