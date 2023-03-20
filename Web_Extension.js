// ==UserScript==
// @name              DE_Apply_Extension
// @namespace         https://github.com/INFWOLAD/DE_Apply
// @version           Mar.20.2
// @author            cosz(INFWOLAD)
// @description       Only For Test.
// @license           AGPL-3.0-or-later
// @match             *://www.qtermin.de/qtermin-stadt-duisburg-abh-sued*
// @grant             none
// @icon              data:image/webp;base64,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
// ==/UserScript==

// Part 1 Start
function input_value() {
  const DE_id = DE_ids.split("&");
  const DE_value = DE_values.split("&");

  for (let i = 0; i <= 8; i++) {
    document.getElementById(DE_id[i].toString()).value = DE_value[i].toString();
  }
  let flag = document.querySelectorAll(".iti__selected-flag");
  flag[0].innerHTML = `<div class="iti__selected-flag" role="combobox" aria-owns="iti-0__country-listbox" aria-expanded="false" tabindex="0" title="Germany (Deutschland): +49" aria-activedescendant="iti-0__item-de-preferred"><div class="iti__flag iti__de"></div><div class="iti__arrow"></div></div>`;
}
// Part 1 End

function add_info(info) {
  if (times < 1) {
    times = times + 1;
    let parent = document.querySelectorAll(".chkBox")[2].parentNode;
    let dom = document.createElement("div");
    dom.className = "sumHeader";
    dom.innerHTML = info;
    parent.insertBefore(
      dom,
      document.querySelectorAll(".chkBox")[2].nextSibling
    );
  }
}

function addButton() {
  let footer = document.getElementById("footer");
  footer.innerHTML = `<div class="footer showFlex" id="footer" style="bottom: 0px;">
    <div class="divbackButton" style="">
      <button id="btnBack" class="btn btn-orange" onclick="showPage(2, true); $('.timeslot').removeClass('timeslotsel'); $('.timeslot').attr('aria-checked', 'false'); return false;">
        Zurück
      </button>
    </div>
    <div id="divWizard" class="wizard">
      <div class="step1" onclick="showPage(1, true); return false;">
        <svg xmlns="http://www.w3.org/2000/svg" class="sumIcon" width="1.25em" height="1.25em">
          <circle class="sumBookingsIcon" fill="#f45917" r="0.5625em" cx="0.625em" cy="0.625em"></circle>
          <text y="50%" text-anchor="middle" x="50%" fill="white" font-size="0.75em" dy="0.30em">1</text>
        </svg>
        <span id="SelServicesFooter" class="wizardText">
          Leistungen</span>
      </div>
      <span class="next">&gt;</span>
      <div class="step2" onclick="showPage(2, true); return false;" style="opacity: 1;">
        <svg xmlns="http://www.w3.org/2000/svg" class="sumIcon" width="1.25em" height="1.25em">
          <circle class="sumBookingsIcon" fill="#f45917" r="0.5625em" cx="0.625em" cy="0.625em"></circle>
          <text y="50%" text-anchor="middle" x="50%" fill="white" font-size="0.75em" dy="0.30em">2</text>
        </svg>
        <span id="SelAppFooter" class="wizardText">
          Termin wählen</span>
      </div>
      <span class="next">&gt;</span>
      <div class="step3" onclick="showPage(3, true); return false;" style="opacity: 1;">
        <svg xmlns="http://www.w3.org/2000/svg" class="sumIcon" width="1.25em" height="1.25em">
          <circle class="sumBookingsIcon" fill="#f45917" r="0.5625em" cx="0.625em" cy="0.625em"></circle>
          <text y="50%" text-anchor="middle" x="50%" fill="white" font-size="0.75em" dy="0.30em">3</text>
        </svg>
        <span class="wizardText">
          Daten eingeben</span>
      </div>
    </div>

    <button id="bp1" class="btn btn-orange" style="display: none;" onclick="return showPage(2, false)">
      Weiter zur Terminauswahl
    </button>
    <button id="bp2" class="btn btn-orange" style="display: none;" onclick="return showPage(3, false)">
      Weiter zur Dateneingabe
    </button>
    <button id='AutoFullfill' class='btn btn-orange' style='' onclick=''>自动填充</button>
    <button id="cmdBookAppointment" class="btn btn-orange" style="" onclick="return showPage(4, false)">Termin reservieren</button>
    <button id="cmdNewApp" class="btn btn-orange" style="display: none" onclick="return bookAgain()">
      Weiteren Termin buchen
    </button>
    <button id="cmdExecRequestAccess" class="btn btn-orange" style="display: none" onclick="return execRequestAccess()">
      Zugang anfordern
    </button>
    <button id="cmdRegList" class="btn btn-orange" style="display: none" onclick="return regList()">
      Auf Vormerkliste eintragen
    </button>
    <button id="cmdNegativeApp" class="btn btn-orange" style="display: none" onclick="return negativeApp()">
      Keine Terminbuchung
    </button>
  </div>`;
}

const DE_ids =
  "Salutation&FirstName&LastName&Email&Birthday&Street&ZIP&City&Phone";
// 请在下面将对应的个人信息用'&'连接起来
const DE_values = "";
const Mode = "Auto";

const targetNode = document.getElementById("divFields");
const config = { childList: true };

let times = 0;

const callback = function (mutationsList, observer) {
  for (let mutation of mutationsList) {
    if (mutation.type === "childList") {
      if (Mode == "Manual") {
        console.log("监测到名额，已注入按钮");
        addButton();
        add_info("先点击自动填写，再点击上面的按钮，最后提交即可");
        let button_add = document.getElementById("AutoFullfill");
        button_add.addEventListener("click", input_value);
      } else {
        add_info("已完成填写，点击上面的按钮，随后提交即可");
        input_value();
      }
    }
  }
};

const observer = new MutationObserver(callback);
observer.observe(targetNode, config);
console.log("注入程序加载完成");
