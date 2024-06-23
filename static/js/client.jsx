import "core-js/stable";
import "regenerator-runtime/runtime";
import $ from './mekoros/mekorosJquery';
import React from 'react';
import ReactDOM from 'react-dom';
import DjangoCSRF from './lib/django-csrf';
const MekorosReact = require('./ReaderApp');
import * as Sentry from "@sentry/react";


$(function() {
  // Initialize Sentry, sentryDSN is defined in base.html
  if (sentryDSN) {
    Sentry.init({
      dsn: sentryDSN,
      integrations: [
        new Sentry.BrowserTracing(),
        new Sentry.Replay(),
      ],
      // Performance Monitoring
      tracesSampleRate: 0.0, // Capture 100% of the transactions, reduce in production!
      // Session Replay
      replaysSessionSampleRate: 0.1, // This sets the sample rate at 10%. You may want to change it to 100% while in development and then sample at a lower rate in production.
      replaysOnErrorSampleRate: 1.0, // If you're not already sampling the entire session, change the sample rate to 100% when sampling sessions where errors occur.
    });
  }

  let container = document.getElementById('s2');
  const loadingPlaceholder = document.getElementById('appLoading');
  const footerContainer = document.getElementById('footerContainer');
  let component = null;
  DjangoCSRF.init();
  var renderFunc = ReactDOM.hydrate;
  if (loadingPlaceholder){
    renderFunc = ReactDOM.render;
  }
  if (DJANGO_VARS.inReaderApp) {
    // Rendering a full ReaderApp experience
    Mekoros.unpackDataFromProps(DJANGO_VARS.props);
    component = React.createElement(MekorosReact.ReaderApp, DJANGO_VARS.props);

    renderFunc(component, container);

  } else {
    // Rendering the Header & Footer only on top of a static page
    let staticProps = {
      multiPanel: $(window).width() > 600,
      headerMode: true,
    };

    let mergedStaticProps = { ...DJANGO_VARS.props, ...staticProps };
    Mekoros.unpackDataFromProps(mergedStaticProps);
    component = React.createElement(MekorosReact.ReaderApp, mergedStaticProps);
    renderFunc(component, container);
    if (footerContainer){
      renderFunc(React.createElement(MekorosReact.Footer), footerContainer);
    }
  }

  if (DJANGO_VARS.containerId && DJANGO_VARS.reactComponentName) {
    // Render a specifc component to a container
    container = document.getElementById(DJANGO_VARS.containerId);
    component = React.createElement(MekorosReact[DJANGO_VARS.reactComponentName], DJANGO_VARS.props);
    renderFunc(component, container);
  }

});
