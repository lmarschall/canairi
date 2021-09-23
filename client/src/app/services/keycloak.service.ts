import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class KeycloakService {

  access_token: string = "";
  refresh_token: string = "";
  username: string = "";
  interval_id: any;
  interval_delta: number = 60000;

  constructor(private http: HttpClient) { }

  /**
   * Retrieves the currently active user token, if existing
   * @returns The access token
   */
  public async getUserToken(): Promise<string> {

    // check if token is expired

    // if access token already defined return
    if(this.access_token != "") {
      return this.access_token;
    } else {
      return "";
    }
  }

  /**
   * Main login function, if successful, sets a few properties in the UserDataService.
   * @param username Username entered by the user
   * @param password Password entered by the user
   * @returns True on successful login
   */
  public async login(username: string, password: string): Promise<boolean>
  {
    try
    {
      // no access token defined, request new access token
      const login_result: any = await this.requestUserToken(username, password);

      // save access token and return
      this.access_token = login_result["access_token"];

      const result: any = await this.requestPermissionToken();

      console.log(result);
      
      // retrieve refresh token from result
      if(result.hasOwnProperty("refresh_token")) {
        console.log("Refresh Token:", result["refresh_token"]);
        this.refresh_token = result["refresh_token"];
      }

      // check if access token in result
      if(result.hasOwnProperty('access_token')) {

        // save access token and return
        this.access_token = result["access_token"];

        console.log("AT is:", this.access_token);
      }

      // Set Access Bool Timer and Refresh Timer
      // setTimeout(() => { this._accessToken_active = false; }, (this._token.expires_in * this.active_tolerance)); // sec * 90% * 1000 [ms]
      // setTimeout(this.refresh_Token.bind(this), (this._token.refresh_expires_in * this.refresh_tolerance)); // sec * 80% * 1000 [ms]
      // this.interval_id = setInterval(() => {this.refresh.bind(this); }, 5000);
      this.interval_id = setInterval(() => {this.refresh(); }, this.interval_delta);

      return true;
    } catch(exception) {
      console.log("Login not successful.");
      return false;
    }
  }

  public logout()
  {
    this.access_token = "";
    this.refresh_token = "";

    // reset refreshment timer if logout occurs
    clearInterval(this.interval_id);
    
  }

  private async refresh(): Promise<void>
  {
    try {
      console.log("try refresh")
      const result: any = await this.refreshUserToken();
      console.log(result)

      // check if access token in result
      if(result.hasOwnProperty('access_token')) {
        
        console.log("Access Token:", result["access_token"]);
        // save access token and return
        this.access_token = result["access_token"];
      }

      // retrieve refresh token from result
      if(result.hasOwnProperty("refresh_token")) {
        console.log("Refresh Token:", result["refresh_token"]);
        this.refresh_token = result["refresh_token"];
      }
    }
    catch {
      console.log("Refresh failed.")
    }
  }

  /**
   * Performs the HTTP request for logging in a user
   * @param username 
   * @param password 
   * @returns the result of the HTTP request
   */
  private async requestUserToken(username: string, password: string) {

    const clientId = environment.keycloak.clientId;
    const realm = environment.keycloak.realm
    const issuer = environment.keycloak.issuer
    const url: string = issuer + '/auth/realms/' + realm + '/protocol/openid-connect/token'

    const params = new HttpParams()
      .set('grant_type', 'password')
      .set('client_id', clientId)
      .set('username', username)
      .set('password', password);

    return this.http.post(url, params, { headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).toPromise();
  }

  /**
   * Performs the HTTP request for refreshing the user token
   * @returns the result of the HTTP request
   */
  private async refreshUserToken() {

    const clientId = environment.keycloak.clientId;
    const realm = environment.keycloak.realm
    const issuer = environment.keycloak.issuer
    const url: string = issuer + '/auth/realms/' + realm + '/protocol/openid-connect/token'

    const params = new HttpParams()
      .set('grant_type', 'refresh_token')
      .set('client_id', clientId)
      .set('refresh_token', this.refresh_token)

    return this.http.post(url, params, { headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).toPromise();
  }

  private async requestPermissionToken() {

    const realm = environment.keycloak.realm
    const issuer = environment.keycloak.issuer
    const url: string = issuer + '/auth/realms/' + realm + '/protocol/openid-connect/token'
    const bearer: string = 'Bearer ' + this.access_token

    const headers = new HttpHeaders()
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .set('Authorization', bearer)

    const params = new HttpParams()
      .set('grant_type', 'urn:ietf:params:oauth:grant-type:uma-ticket')
      .set('audience', "django-rest-api")
      .set('permission', "Measurement#measurement:get")

    return this.http.post(url, params, { headers: headers}).toPromise();
  }
}
