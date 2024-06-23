import React  from 'react';
import Mekoros  from './mekoros/mekoros';
import PropTypes from'prop-types';
import $  from './mekoros/mekorosJquery';
import { InterfaceText, DonateLink } from './Misc';
import {NewsletterSignUpForm} from "./NewsletterSignUpForm";
import Component from 'react-class';

const Section = ({en, he, children}) => (
    <div className="section">
      <div className="header">
         <InterfaceText text={{en:en, he:he}}/>
      </div>
      {children}
    </div>
);

const Link = ({href, en, he, blank}) => (
    <a href={href} target={blank ? "_blank" : "_self"}>
      <InterfaceText text={{en:en, he:he}}/>
    </a>
);

class Footer extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  componentDidMount() {
    this.setState({isClient: true});
  }
  trackLanguageClick(language){
    Mekoros.track.setInterfaceLanguage('interface language footer', language);
  }
  render() {
    if (!Mekoros._siteSettings.TORAH_SPECIFIC) { return null; }

    const fbURL = Mekoros.interfaceLang == "hebrew" ? "https://www.facebook.com/mekoros.com" : "https://www.facebook.com/mekoros.com";
    const blgURL = Mekoros.interfaceLang == "hebrew" ? "https://blog.mekoros.com/" : "https://blog.mekoros.com/";
    let next = this.state.isClient ? (encodeURIComponent(Mekoros.util.currentPath())) : "/" ; //try to make sure that a server render of this does not get some weird data in the url that then gets cached
    return (
      <footer id="footer" className="static sans-serif">
        <div id="footerInner">
            <Section en="About" he="אודות">
                <Link href="/about" en="What is Mekoros?" he="מהי ספריא" />
                <Link href="/help" en="Help" he="עזרה" />
                <Link href="/team" en="Team" he="צוות" />
                <Link href="/testimonials" en="Testimonials" he="חוות דעת" />
                <Link href="/metrics" en="Metrics" he="מדדים" />
                <Link href="/annualreport" en="Annual Report" he='דו"ח שנתי' />
                <Link href="/terms" en="Terms of Use" he="תנאי שימוש" />
                <Link href="/privacy-policy" en="Privacy Policy" he="מדיניות פרטיות" />
            </Section>

            <Section en="Tools" he="כלים">
                <Link href="/educators" en="Teach with Mekoros" he="מלמדים עם ספריא" />
                <Link href="/calendars" en="Learning Schedules" he="לוח לימוד יומי" />
                <Link href="/sheets" en="Source Sheets" he="דפי מקורות" />
                <Link href="/visualizations" en="Visualizations" he="תרשימים גרפיים" />
                <Link href="/mobile" en="Mobile Apps" he="ספריא בנייד" />
                <Link href="/daf-yomi" en="Daf Yomi" he="דף יומי" />
                <Link href="/torah-tab" en="Torah Tab" he="תורה טאב" />
                <Link href="/people" en="Authors" he="מחברים" />
                <Link href="/collections" en="Collections" he="אסופות" />
                <Link href="/updates" en="New Additions" he="עדכונים" />
                <Link href="/remote-learning" en="Remote Learning" he="למידה מרחוק" />
            </Section>

            <Section en="Developers" he="מפתחים">
                <Link href="https://developers.mekoros.com" en="Get Involved" he="הצטרפו אלינו" blank={true} />
                <Link href="https://developers.mekoros.com/reference" en="API Docs" he="מסמכי API" blank={true} />
                <Link href="https://github.com/Mekoros/Mekoros-Project" en="Fork us on GitHub" he="Github" blank={true} />
                <Link href="https://github.com/Mekoros/Mekoros-Export" en="Download our Data" he="בסיס נתונים" blank={true} />
            </Section>

            <Section en="Join Us" he="הצטרפו אלינו">
                <DonateLink source={"Footer"}><InterfaceText text={{en:"Donate", he:"תרומות"}}/></DonateLink>
                <Link href="/ways-to-give" en="Ways to Give" he="אפשרויות תרומה" />
                <Link href="/supporters" en="Supporters" he="תומכים" />
                <Link href="/jobs" en="Jobs" he="דרושים" />
                <Link href="https://store.mekoros.com" en="Shop" he="חנות" />
            </Section>

          <div className="section last connect">
              <div className="header connect">
                  <InterfaceText>Connect</InterfaceText>
              </div>
              <NewsletterSignUpForm contextName="Footer" />
              <div className="socialLinks">
                  <Link href="https://www.instagram.com/mekorosproject/" en="Instagram" he="אינסטגרם" blank={true} />
                  &bull;
                  <Link href={fbURL} en="Facebook" he="פייסבוק" blank={true} />
                  <br />

                  <Link href="https://www.youtube.com/user/MekorosProject" en="YouTube" he="יוטיוב" blank={true} />
                  &bull;
                  <Link href={blgURL} en="Blog" he="בלוג" blank={true}/>
                  <br />

                  <Link href="https://www.linkedin.com/company/mekoros/" en="LinkedIn" he="לינקדאין" blank={true} />
                  &bull;
                  <Link href="mailto:hello@mekoros.com" en="Email" he="דוא&quot;ל" />
              </div>
              <div id="siteLanguageToggle">
                  <div id="siteLanguageToggleLabel">
                      <InterfaceText>Site Language</InterfaceText>
                  </div>
                  <a href={"/interface/english?next=" + next} id="siteLanguageEnglish"
                     onClick={this.trackLanguageClick.bind(null, "English")}>English
                  </a>
                  |
                  <a href={"/interface/hebrew?next=" + next} id="siteLanguageHebrew"
                      onClick={this.trackLanguageClick.bind(null, "Hebrew")}>עברית
                  </a>
              </div>
          </div>
        </div>
      </footer>
    );
  }
}

export default Footer;
