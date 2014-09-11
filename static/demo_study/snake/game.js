

function save_data_success(data) 
{
    if (data == "SUCCESS") {
        // we successfully saved the data
        window.location = "/study/fsess";
    } else {
        // Something went wrong with the tangra server... what do we do?
        alert("ERROR: couldn't save data on the Tangra server!");
    }
}


function save_data_failure(data) 
{
    alert("FAILURE! " + data)
}


function save_tangra_data(data)
{
    $.ajax({
                type:"POST",
                url: "/public_api/save_data",
                data: {"data" : data},
                success : save_data_success,
                error : save_data_failure
            });
}


function gamerun() {
  init();
}

function step(){
  update();
  draw();
}

function update() {
  if (!movesnake()) {
    die();
    
    $("#message_1").html("Saving data. please wait...");
    $("#message_2").html("");
    window.setTimeout(function() { save_tangra_data("snake_score: " + size) }, 1000)
    
    
  }
}

function draw() {
  screenclear();
  drawsnake();
  drawfood();
}