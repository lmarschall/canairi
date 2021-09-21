import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SensorsService {

  constructor(private http: HttpClient) { }

  public async getSensorValues(user_token: string): Promise<JSON> {

    const result: JSON = await this.requestSensorValues(user_token);

    return result;
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

  private async requestSensorValues(user_token: string): Promise<JSON> {

    const url: string = 'http://0.0.0.0:8000/measurements/get'

    const data = new HttpParams()
    .set('data', user_token)

    // var data = {
    //   'Token': user_token
    // }

    return await this.http.get<JSON>(url).toPromise()
  }
}
