/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffeshop-api.us', // the auth0 domain prefix
    audience: 'coffeshop', // the audience set for the auth0 app
    clientId: 'Xs3BKIZy1I5POGTEceLf4mNv6IzlrRCD', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application. 
  }
};
