import { searchFeature } from './features.js';

(() => {
	document.getElementById('search-btn').onclick = () => {
		searchFeature.doSearch();
	};

	document.getElementById('reset-btn').onclick = () => {
		searchFeature.reset();
	};

	document.getElementById('search-bar').onkeypress = (e) => {
		if (e.key === 'Enter') {
			searchFeature.doSearch(e.target.value);
		}
	};
})();