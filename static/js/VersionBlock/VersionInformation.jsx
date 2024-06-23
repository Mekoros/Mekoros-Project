import React from 'react';
import PropTypes from 'prop-types';
import classNames from "classnames";
import Mekoros from "../mekoros/mekoros";
import {VersionBlockUtils} from './VersionBlock';

function VersionInformation({currentRef, version}) {
    function makeLicenseLink() {
        const license_map = Mekoros.getLicenseMap();
        return (version.license in license_map) ? license_map[version.license] : "#";
    }
    return (
        <div className="versionDetailsInformation">
            <div className={classNames(VersionBlockUtils.makeAttrClassNames(version, {"versionSource": 1, "versionDetailsElement": 1}, "versionSource"))}>
              <span className="versionDetailsLabel">
                {`${Mekoros._("Source")}: `}
              </span>
              <a className="versionDetailsLink" href={version.versionSource} target="_blank">
                { Mekoros.util.parseUrl(version.versionSource).host.replace("www.", "") }
              </a>
            </div>
            <div className={classNames(VersionBlockUtils.makeAttrClassNames(version, {"versionDigitizedByMekoros": 1, "versionDetailsElement": 1}, "digitizedByMekoros"))}>
              <span className="versionDetailsLabel">
                {`${Mekoros._("Digitization")}: `}
              < /span>
              <a className="versionDetailsLink" href="/digitized-by-mekoros" target="_blank">
                {Mekoros._("Mekoros")}
              </a>
            </div>
            <div className={classNames(VersionBlockUtils.makeAttrClassNames(version, {"versionLicense": 1, "versionDetailsElement": 1}, "license" ))}>
              <span className="versionDetailsLabel">
                {`${Mekoros._("License")}: `}
              </span>
              <a className="versionDetailsLink" href={makeLicenseLink()} target="_blank">
                {Mekoros._(version?.license)}
              </a>
            </div>
            <div className={classNames(VersionBlockUtils.makeAttrClassNames(version, {"versionHistoryLink": 1, "versionDetailsElement": 1}, null))}>
               <a className="versionDetailsLink" href={`/activity/${Mekoros.normRef(currentRef)}/${version.language}/${version.versionTitle && version.versionTitle.replace(/\s/g,"_")}`} target="_blank">
                 {Mekoros._("Revision History")}
               </a>
            </div>
            <div className={classNames(VersionBlockUtils.makeAttrClassNames(version, {"versionBuyLink": 1, "versionDetailsElement": 1}, "purchaseInformationURL"))}>
               <a className="versionDetailsLink" href={version.purchaseInformationURL} target="_blank">
                {Mekoros._("Buy in Print")}
               </a>
            </div>
        </div>
    );
}
VersionInformation.prototypes = {
    currentRef: PropTypes.string.isRequired,
    version: PropTypes.object.isRequired,
};
export default VersionInformation;
