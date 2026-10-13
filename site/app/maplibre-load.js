// The web map's MapLibre, loaded by FigMap.web.tsx: a module script from FIG's own site, so the page's security policy
// needs no eval. Keep the version the same as FigMap.web.tsx and package.json.
import * as maplibregl from 'https://cdn.jsdelivr.net/npm/maplibre-gl@6.11.2/dist/maplibre-gl.mjs';

maplibregl.setWorkerUrl(new URL('maplibre-worker.js', import.meta.url).href); // same site as this file
window.maplibregl = maplibregl;
window.dispatchEvent(new Event('fig-maplibre'));
