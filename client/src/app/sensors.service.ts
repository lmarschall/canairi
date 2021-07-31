import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SensorsService {

  constructor(private http: HttpClient) { }

  public async getSensorValues(): Promise<string> {

    const result: JSON = await this.requestSensorValues();

    console.log(result)
    return "";
  }

  // private async requestUserToken(username: string, password: string): Promise<JSON> {

  //   const clientId = environment.keycloak.clientId;
  //   const realm = environment.keycloak.realm
  //   const issuer = environment.keycloak.issuer
  //   const url: string = issuer + '/auth/realms/' + realm + '/protocol/openid-connect/token'

  //   const params = new HttpParams()
  //     .set('grant_type', 'password')
  //     .set('client_id', clientId)
  //     .set('username', username)
  //     .set('password', password);

  //   return await this.http.post<JSON>(url, params, { headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).toPromise()
  // }

  private async requestSensorValues(): Promise<JSON> {

    const url: string = 'http://0.0.0.0:8000/measurements/get'

    return await this.http.get<JSON>(url).toPromise()
  }
}
