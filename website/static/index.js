


/*
    this method figures out which note to be deleted using note id
    note id is being specified from the note.data list column row

    takse note id passed and makes a POST request to the delete-note endpoint
    once response -> reloads the window

 */

function deleteNote(noteId){

    fetch("/delete-note", { 
        method: "POST",
        body: JSON.stringify({noteId: noteId}),
    }).then ((_res) => {
        window.location.href = "/" //reloads the window once response received
    });
}