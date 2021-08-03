import { Component, OnInit, ViewChild } from '@angular/core';
import { SensorsService } from 'src/app/sensors.service';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { multi } from './data';
import {FormGroup, FormControl} from '@angular/forms';
// import * as pluginAnnotations from 'chartjs-plugin-annotation';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  range = new FormGroup({
    start: new FormControl(),
    end: new FormControl()
  });

  air_quality: number = 0
  temperature: number = 0.0
  humidity: number = 0.0


  interval_id: any

  multi: any[] = [];
  view: [number, number] = [700, 300];

  // options
  legend: boolean = true;
  showLabels: boolean = true;
  animations: boolean = true;
  xAxis: boolean = true;
  yAxis: boolean = true;
  showYAxisLabel: boolean = true;
  showXAxisLabel: boolean = true;
  xAxisLabel: string = 'Year';
  yAxisLabel: string = 'Population';
  timeline: boolean = true;

  colorScheme = {
    domain: ['#5AA454', '#E44D25', '#CFC0BB', '#7aa3e5', '#a8385d', '#aae3f5']
  };

  constructor(private readonly sensors: SensorsService){Object.assign(this, { multi })}

  ngOnInit(): void {

    console.log("init")

    this.interval_id = setInterval(() => {this.loop(); }, 5000);
  }

  ngOnDestroy() {
    if (this.interval_id) {
      clearInterval(this.interval_id);
    }
  }

  public loop(): void {
    this.getSensorValues()
  }

  public async getSensorValues() {

    console.log("get sensor values")
    const values = await this.sensors.getSensorValues();

    interface Measurement {
      id: number;
      air_quality: number;
      gas_resistance: number;
      humidity: number;
      pressure: number;
      temperature: number;
      time: string;
    }

    var measurements = <Measurement[]><unknown>values;

    this.air_quality = measurements[0].air_quality
    this.temperature = measurements[0].temperature
    this.humidity = measurements[0].humidity
    
    // first_element = values
    console.log(measurements);
  }

  onSelect(data: any): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  }

  onActivate(data: any): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  onDeactivate(data: any): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

}
