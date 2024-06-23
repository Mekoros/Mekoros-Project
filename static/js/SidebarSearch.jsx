import { useState, useEffect } from "react";
import {InterfaceText, EnglishText, HebrewText} from "./Misc";
import Mekoros from "./mekoros/mekoros";
import SearchState from './mekoros/searchState';
import SearchResultList  from './SearchResultList';
import DictionarySearch  from './DictionarySearch';
import classNames from 'classnames';

import {
  SearchButton,
} from './Misc';


const SidebarSearch = ({ title, updateAppliedOptionSort, navigatePanel, sidebarSearchQuery, setSidebarSearchQuery, onSidebarSearchClick }) => {
  const [lexiconName, setLexiconName] = useState(Mekoros.getIndexDetailsFromCache(title)?.lexiconName)
  const [searchFilterPathForBook, setSearchFilterPathForBook] = useState('');
  const [query, setQuery] = useState(sidebarSearchQuery || '');
  const isDictionary = !!lexiconName;
  const [searchState, setSearchState] = useState(
          new SearchState({
                  type: 'text',
                  appliedFilters:        [searchFilterPathForBook],
                  field:                 "naive_lemmatizer",
                  appliedFilterAggTypes: ["path"],
                  sortType:              "chronological",
          })
      )

  useEffect(() => {
      attachKeyboard();
      const searchInput = document.getElementById('searchQueryInput')
      if (searchInput) {
          searchInput.value = query
      }
  }, []);

  useEffect(() => {
      Mekoros.bookSearchPathFilterAPI(title).then((path) => {
        setSearchFilterPathForBook(path)
      })
      setSidebarSearchQuery(query)
  }, [query])

  useEffect(() => {
      setSearchState(
        new SearchState({
                type: 'text',
                appliedFilters:        [searchFilterPathForBook],
                field:                 "naive_lemmatizer",
                appliedFilterAggTypes: ["path"],
                sortType:              "chronological",
                filtersValid: true,
        })
      )
  }, [searchFilterPathForBook])

   const attachKeyboard = () => {
      const inputElement = document.querySelector('.sidebarSearch input');
      if (inputElement && (!inputElement.VKI_attached)) {
        VKI_attach(inputElement);
      }
    }


  const inputClasses = classNames({
    search: 1,
    serif: 1,
    keyboardInput: Mekoros.interfaceLang === "english",
    hebrewSearch: Mekoros.interfaceLang === "hebrew"
    });
  // const searchBoxClasses = classNames({searchBox: 1, searchFocused: this.state.searchFocused});
  const searchBoxClasses = classNames({searchBox: 1});

  const handleSearchButtonClick = () => {
    const searchBoxValue = document.getElementById('searchQueryInput').value
    if (searchBoxValue !== query) {
      setSearchFilterPathForBook('')
      setQuery(document.getElementById('searchQueryInput').value)
    }
  }


  return (
    <div className="sidebarSearch lexicon-content">
    <div className={searchBoxClasses}>

    { isDictionary ?
       <DictionarySearch
            lexiconName={lexiconName}
            title={title}
            navigatePanel={navigatePanel}
            contextSelector=".lexicon-content"/>
      :
      <>
        <SearchButton onClick={handleSearchButtonClick} />
        <input className={inputClasses}
          placeholder={Mekoros._("Search in this text")}
          id="searchQueryInput"
          maxLength={75}
          onKeyUp={
            (event) => {
              if (event.keyCode === 13) {
                handleSearchButtonClick()
              }
            }
          }
          title={Mekoros._("Search in this text")} />
      </>
      }

    </div>


      {query ?
        <SearchResultList
          query={query}
          compare={false}
          searchInBook={true}
          tab="text"
          types={["text"]}
          textSearchState={searchState}
          updateTotalResults={n => console.log(n)}
          registerAvailableFilters={n => console.log(n)}
          updateAppliedOptionSort={updateAppliedOptionSort}
          onResultClick={onSidebarSearchClick}
        /> :

        null

    }


    </div>
  );



}




export default SidebarSearch;
