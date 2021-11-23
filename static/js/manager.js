function savingThrow(value, id) {
    // Rows a saving throw
    postWithAxios("/character/check", {"value": value, "id": id, 'saving': 1}, displayRoll, value);
}

function Check(value, id) {
    // Rows a check
    postWithAxios("/character/check", {"value": value, "id": id}, displayRoll, value);
}

function displayRoll(request) {
    alert("You've rolled a "  + request.data.result);
}

function Skill(value, id) {
    // Rolls a skill check
    postWithAxios("/character/skill_check", {"value": value, "id": id}, displayRoll, value)
}

function AddWeapon(char_id){
    let table = document.getElementById("table_weapons");
    postWithAxios("/character/get_html_weapon", {'number_row': table.childElementCount}, AftAddWeapon, null)
}

function AddItem(char_id){
    let table = document.getElementById("table_inventory");
    postWithAxios("/character/get_html_item", {'number_row': table.childElementCount}, AftAddItem, null)
}


function AftAddWeapon(html){
    let table = document.getElementById("table_weapons");
    table.innerHTML += html.data.data;
}

function AftAddItem(html){
    let table = document.getElementById("table_inventory");
    table.innerHTML += html.data.data;
}

function saveWeapon(weapon_row){
    let weapon_name = document.getElementById('weapon_name_' + weapon_row).value
    let weapon_dmg = document.getElementById('weapon_damage_' + weapon_row).value
    let weapon_data = {'weapon_name': weapon_name, 'weapon_damage': weapon_dmg}
    postWithAxios("/character/save_weapon", weapon_data, reload, weapon_data)
}

function saveItem(item_row){
    let item_name = document.getElementById('item_name_' + item_row).value;
    let item_description = document.getElementById('item_description_' + item_row).value;
    let item_weight = document.getElementById('item_weight_' + item_row).value;
    let item_data = {'item_name': item_name, 'item_description': item_description, 'item_weight': item_weight}
    postWithAxios('/character/save_item', item_data, reload, item_data);
}

function rollWeaponDamage(weapon_id){
    postWithAxios("/character/roll_weapon_damage", {'weapon_id': weapon_id}, displayRoll)
}

function attrSaveProficiency(value, id, input) {
    // Saves if proficient with an stat
    let proficiency = 1;
    if (!input.checked) {
        proficiency = 0
    }
    postWithAxios("/character/save_proficiency", {
        "attribute": value,
        "id": id,
        "proficiency": proficiency
    }, reload, value)
}

function saveProficiency(skill, id, input) {
    // Saved the proficiency with a skill
    let proficiency = 1;
    if (!input.checked) {
        proficiency = 0
    }
    postWithAxios("/character/save_proficiency", {"skill": skill, "id": id, "proficiency": proficiency}, reload, skill)
}

function reload(request) {
    if (request.data.reload === 1) {
        window.location.reload();
    }
}

function postWithAxios(url, data, method, param) {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios.post(url, {
        data
    })
        .then(function (response) {
            if (method) return method(response, param);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function getWithAxios(url, method, param) {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios({
        method: 'get',
        url: url,
        responseType: 'stream'
    })
        .then(function (response) {
            if (method) return method(response, param);
        })
        .catch(function (error) {
            console.log(error);
        });
}