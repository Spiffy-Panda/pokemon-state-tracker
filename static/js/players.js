// JavaScript for Players page

// Global variables
let currentPlayerId = null;
let currentPage = 1;
const perPage = 10;

// DOM Elements
const playersTableBody = document.getElementById('playersTableBody');
const pagination = document.getElementById('pagination');
const addPokemonBtn = document.getElementById('addPokemonBtn');
const savePlayerBtn = document.getElementById('savePlayerBtn');
const teamContainer = document.getElementById('teamContainer');

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Load players
    await loadPlayers();
    
    // Set up event listeners
    if (addPokemonBtn) {
        addPokemonBtn.addEventListener('click', addPokemonInput);
    }
    
    if (savePlayerBtn) {
        savePlayerBtn.addEventListener('click', createPlayer);
    }
    
    // Add initial Pokemon input
    addPokemonInput();
});

// Load players from API
async function loadPlayers() {
    try {
        const result = await apiRequest(`/players/?page=${currentPage}&per_page=${perPage}`);
        
        if (result.success) {
            renderPlayers(result.data);
            renderPagination(result);
        }
    } catch (error) {
        console.error('Error loading players:', error);
    }
}

// Render players table
function renderPlayers(players) {
    playersTableBody.innerHTML = '';
    
    if (players.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `<td colspan="6" class="text-center">No players found</td>`;
        playersTableBody.appendChild(row);
        return;
    }
    
    players.forEach(player => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${player.id}</td>
            <td>${player.name}</td>
            <td>${player.location.location_tuple.join(' - ')}</td>
            <td>${player.team.length} / 6</td>
            <td>${formatDate(player.last_updated)}</td>
            <td>
                <button class="btn btn-sm btn-primary view-player" data-id="${player.id}">View</button>
                <button class="btn btn-sm btn-danger delete-player" data-id="${player.id}">Delete</button>
            </td>
        `;
        playersTableBody.appendChild(row);
    });
    
    // Add event listeners to buttons
    document.querySelectorAll('.view-player').forEach(btn => {
        btn.addEventListener('click', () => viewPlayer(btn.dataset.id));
    });
    
    document.querySelectorAll('.delete-player').forEach(btn => {
        btn.addEventListener('click', () => deletePlayer(btn.dataset.id));
    });
}

// Render pagination controls
function renderPagination(result) {
    pagination.innerHTML = '';
    
    if (result.total_pages <= 1) {
        return;
    }
    
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Page navigation');
    
    const ul = document.createElement('ul');
    ul.className = 'pagination';
    
    // Previous button
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${result.page === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#" ${result.page === 1 ? '' : 'data-page="' + (result.page - 1) + '"'}>Previous</a>`;
    ul.appendChild(prevLi);
    
    // Page numbers
    for (let i = 1; i <= result.total_pages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === result.page ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
        ul.appendChild(li);
    }
    
    // Next button
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${result.page === result.total_pages ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#" ${result.page === result.total_pages ? '' : 'data-page="' + (result.page + 1) + '"'}>Next</a>`;
    ul.appendChild(nextLi);
    
    nav.appendChild(ul);
    pagination.appendChild(nav);
    
    // Add event listeners to pagination links
    document.querySelectorAll('.page-link[data-page]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            currentPage = parseInt(link.dataset.page);
            loadPlayers();
        });
    });
}

// Add Pokemon input to form
function addPokemonInput() {
    const pokemonCount = document.querySelectorAll('.pokemon-input-group').length;
    
    if (pokemonCount >= 6) {
        showAlert('Maximum team size is 6 Pokemon', 'warning');
        return;
    }
    
    const pokemonDiv = document.createElement('div');
    pokemonDiv.className = 'pokemon-input-group card mb-3';
    pokemonDiv.innerHTML = `
        <div class="card-header d-flex justify-content-between align-items-center">
            <h6 class="mb-0">Pokemon #${pokemonCount + 1}</h6>
            ${pokemonCount > 0 ? '<button type="button" class="btn-close remove-pokemon" aria-label="Remove"></button>' : ''}
        </div>
        <div class="card-body">
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label">Name</label>
                    <input type="text" class="form-control pokemon-name" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Level</label>
                    <input type="number" class="form-control pokemon-level" min="1" max="100" value="50" required>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label">Type 1</label>
                    <select class="form-select pokemon-type1" required>
                        <option value="">Select Type</option>
                        <option value="normal">Normal</option>
                        <option value="fire">Fire</option>
                        <option value="water">Water</option>
                        <option value="grass">Grass</option>
                        <option value="electric">Electric</option>
                        <option value="ice">Ice</option>
                        <option value="fighting">Fighting</option>
                        <option value="poison">Poison</option>
                        <option value="ground">Ground</option>
                        <option value="flying">Flying</option>
                        <option value="psychic">Psychic</option>
                        <option value="bug">Bug</option>
                        <option value="rock">Rock</option>
                        <option value="ghost">Ghost</option>
                        <option value="dragon">Dragon</option>
                        <option value="dark">Dark</option>
                        <option value="steel">Steel</option>
                        <option value="fairy">Fairy</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Type 2 (Optional)</label>
                    <select class="form-select pokemon-type2">
                        <option value="">None</option>
                        <option value="normal">Normal</option>
                        <option value="fire">Fire</option>
                        <option value="water">Water</option>
                        <option value="grass">Grass</option>
                        <option value="electric">Electric</option>
                        <option value="ice">Ice</option>
                        <option value="fighting">Fighting</option>
                        <option value="poison">Poison</option>
                        <option value="ground">Ground</option>
                        <option value="flying">Flying</option>
                        <option value="psychic">Psychic</option>
                        <option value="bug">Bug</option>
                        <option value="rock">Rock</option>
                        <option value="ghost">Ghost</option>
                        <option value="dragon">Dragon</option>
                        <option value="dark">Dark</option>
                        <option value="steel">Steel</option>
                        <option value="fairy">Fairy</option>
                    </select>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label">Nature</label>
                    <select class="form-select pokemon-nature" required>
                        <option value="">Select Nature</option>
                        <option value="hardy">Hardy</option>
                        <option value="lonely">Lonely</option>
                        <option value="brave">Brave</option>
                        <option value="adamant">Adamant</option>
                        <option value="naughty">Naughty</option>
                        <option value="bold">Bold</option>
                        <option value="docile">Docile</option>
                        <option value="relaxed">Relaxed</option>
                        <option value="impish">Impish</option>
                        <option value="lax">Lax</option>
                        <option value="timid">Timid</option>
                        <option value="hasty">Hasty</option>
                        <option value="serious">Serious</option>
                        <option value="jolly">Jolly</option>
                        <option value="naive">Naive</option>
                        <option value="modest">Modest</option>
                        <option value="mild">Mild</option>
                        <option value="quiet">Quiet</option>
                        <option value="bashful">Bashful</option>
                        <option value="rash">Rash</option>
                        <option value="calm">Calm</option>
                        <option value="gentle">Gentle</option>
                        <option value="sassy">Sassy</option>
                        <option value="careful">Careful</option>
                        <option value="quirky">Quirky</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Held Item (Optional)</label>
                    <input type="text" class="form-control pokemon-held-item">
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <label class="form-label">Base Stats</label>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="input-group">
                        <span class="input-group-text">HP</span>
                        <input type="number" class="form-control pokemon-stat-hp" min="1" max="255" value="50" required>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="input-group">
                        <span class="input-group-text">Atk</span>
                        <input type="number" class="form-control pokemon-stat-atk" min="1" max="255" value="50" required>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="input-group">
                        <span class="input-group-text">Def</span>
                        <input type="number" class="form-control pokemon-stat-def" min="1" max="255" value="50" required>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="input-group">
                        <span class="input-group-text">SpA</span>
                        <input type="number" class="form-control pokemon-stat-spa" min="1" max="255" value="50" required>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="input-group">
                        <span class="input-group-text">SpD</span>
                        <input type="number" class="form-control pokemon-stat-spd" min="1" max="255" value="50" required>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="input-group">
                        <span class="input-group-text">Spe</span>
                        <input type="number" class="form-control pokemon-stat-spe" min="1" max="255" value="50" required>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    teamContainer.appendChild(pokemonDiv);
    
    // Add event listener to remove button
    const removeBtn = pokemonDiv.querySelector('.remove-pokemon');
    if (removeBtn) {
        removeBtn.addEventListener('click', () => {
            pokemonDiv.remove();
            // Update Pokemon numbers
            document.querySelectorAll('.pokemon-input-group').forEach((group, index) => {
                group.querySelector('h6').textContent = `Pokemon #${index + 1}`;
            });
        });
    }
}

// Create new player
async function createPlayer() {
    try {
        // Validate form
        const playerName = document.getElementById('playerName').value.trim();
        if (!playerName) {
            showAlert('Player name is required', 'danger');
            return;
        }
        
        // Get location data
        const locationArea = document.getElementById('locationArea').value.trim();
        const locationSpecific = document.getElementById('locationSpecific').value.trim();
        const locationDescription = document.getElementById('locationDescription').value.trim();
        
        if (!locationArea || !locationSpecific) {
            showAlert('Location area and specific location are required', 'danger');
            return;
        }
        
        // Get Pokemon data
        const pokemonInputGroups = document.querySelectorAll('.pokemon-input-group');
        const team = [];
        
        for (const group of pokemonInputGroups) {
            const name = group.querySelector('.pokemon-name').value.trim();
            const level = parseInt(group.querySelector('.pokemon-level').value);
            const type1 = group.querySelector('.pokemon-type1').value;
            const type2 = group.querySelector('.pokemon-type2').value;
            const nature = group.querySelector('.pokemon-nature').value;
            const heldItem = group.querySelector('.pokemon-held-item').value.trim();
            
            const hp = parseInt(group.querySelector('.pokemon-stat-hp').value);
            const atk = parseInt(group.querySelector('.pokemon-stat-atk').value);
            const def = parseInt(group.querySelector('.pokemon-stat-def').value);
            const spa = parseInt(group.querySelector('.pokemon-stat-spa').value);
            const spd = parseInt(group.querySelector('.pokemon-stat-spd').value);
            const spe = parseInt(group.querySelector('.pokemon-stat-spe').value);
            
            if (!name || !type1 || !nature) {
                showAlert(`Please fill in all required fields for Pokemon #${team.length + 1}`, 'danger');
                return;
            }
            
            const types = [type1];
            if (type2) {
                types.push(type2);
            }
            
            team.push({
                name,
                level,
                types,
                abilities: [{ name: "Unknown", is_hidden: false }], // Placeholder
                nature,
                held_item: heldItem || null,
                base_stats: {
                    hp,
                    attack: atk,
                    defense: def,
                    special_attack: spa,
                    special_defense: spd,
                    speed: spe
                }
            });
        }
        
        // Create player data
        const playerData = {
            name: playerName,
            location: {
                location_tuple: [locationArea, locationSpecific],
                description: locationDescription || null,
                accessible_locations: []
            },
            team
        };
        
        // Send API request
        const result = await apiRequest('/players/', 'POST', playerData);
        
        if (result.success) {
            showAlert(`Player ${playerName} created successfully`, 'success');
            
            // Close modal and reload players
            const modal = bootstrap.Modal.getInstance(document.getElementById('createPlayerModal'));
            modal.hide();
            
            // Reset form
            document.getElementById('createPlayerForm').reset();
            teamContainer.innerHTML = '';
            addPokemonInput();
            
            // Reload players
            await loadPlayers();
        }
    } catch (error) {
        console.error('Error creating player:', error);
    }
}

// View player details
async function viewPlayer(playerId) {
    try {
        currentPlayerId = playerId;
        const result = await apiRequest(`/players/${playerId}`);
        
        if (result.success) {
            const player = result.data;
            
            // Set modal title
            document.getElementById('playerDetailsTitle').textContent = `Player: ${player.name}`;
            
            // Load team tab content
            loadTeamTab(player);
            
            // Load location tab content
            loadLocationTab(player);
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('playerDetailsModal'));
            modal.show();
            
            // Add event listeners for tab changes
            document.querySelectorAll('button[data-bs-toggle="tab"]').forEach(button => {
                button.addEventListener('shown.bs.tab', async (event) => {
                    const targetId = event.target.getAttribute('data-bs-target').substring(1);
                    
                    if (targetId === 'thoughts') {
                        await loadThoughtsTab(player.id);
                    } else if (targetId === 'battles') {
                        await loadBattlesTab(player.id);
                    } else if (targetId === 'matchups') {
                        await loadMatchupsTab(player.id);
                    }
                });
            });
        }
    } catch (error) {
        console.error('Error viewing player:', error);
    }
}

// Load team tab content
function loadTeamTab(player) {
    const teamContent = document.getElementById('teamContent');
    teamContent.innerHTML = '';
    
    if (player.team.length === 0) {
        teamContent.innerHTML = '<div class="col-12"><p class="text-center">No Pokemon in team</p></div>';
        return;
    }
    
    player.team.forEach(pokemon => {
        const pokemonCard = document.createElement('div');
        pokemonCard.className = 'col-md-4 mb-4';
        
        // Calculate stat percentages (based on max 255)
        const hpPercent = (pokemon.base_stats.hp / 255) * 100;
        const atkPercent = (pokemon.base_stats.attack / 255) * 100;
        const defPercent = (pokemon.base_stats.defense / 255) * 100;
        const spaPercent = (pokemon.base_stats.special_attack / 255) * 100;
        const spdPercent = (pokemon.base_stats.special_defense / 255) * 100;
        const spePercent = (pokemon.base_stats.speed / 255) * 100;
        
        // Create type badges
        const typeBadges = pokemon.types.map(type => 
            `<span class="type-badge type-${type.toLowerCase()}">${type}</span>`
        ).join('');
        
        pokemonCard.innerHTML = `
            <div class="card pokemon-card">
                <div class="card-header bg-primary text-white">
                    ${pokemon.name} (Lv. ${pokemon.level})
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        ${typeBadges}
                    </div>
                    <p><strong>Nature:</strong> ${pokemon.nature}</p>
                    ${pokemon.held_item ? `<p><strong>Held Item:</strong> ${pokemon.held_item}</p>` : ''}
                    <p><strong>HP:</strong> ${pokemon.current_hp}/${pokemon.max_hp}</p>
                    
                    <h6 class="mt-3">Stats:</h6>
                    <div class="mb-2">
                        <small>HP: ${pokemon.base_stats.hp}</small>
                        <div class="stats-bar">
                            <div class="stats-bar-fill bg-success" style="width: ${hpPercent}%"></div>
                        </div>
                    </div>
                    <div class="mb-2">
                        <small>Attack: ${pokemon.base_stats.attack}</small>
                        <div class="stats-bar">
                            <div class="stats-bar-fill bg-danger" style="width: ${atkPercent}%"></div>
                        </div>
                    </div>
                    <div class="mb-2">
                        <small>Defense: ${pokemon.base_stats.defense}</small>
                        <div class="stats-bar">
                            <div class="stats-bar-fill bg-warning" style="width: ${defPercent}%"></div>
                        </div>
                    </div>
                    <div class="mb-2">
                        <small>Sp. Attack: ${pokemon.base_stats.special_attack}</small>
                        <div class="stats-bar">
                            <div class="stats-bar-fill bg-info" style="width: ${spaPercent}%"></div>
                        </div>
                    </div>
                    <div class="mb-2">
                        <small>Sp. Defense: ${pokemon.base_stats.special_defense}</small>
                        <div class="stats-bar">
                            <div class="stats-bar-fill bg-primary" style="width: ${spdPercent}%"></div>
                        </div>
                    </div>
                    <div class="mb-2">
                        <small>Speed: ${pokemon.base_stats.speed}</small>
                        <div class="stats-bar">
                            <div class="stats-bar-fill bg-secondary" style="width: ${spePercent}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        teamContent.appendChild(pokemonCard);
    });
}

// Load location tab content
function loadLocationTab(player) {
    const locationContent = document.getElementById('locationContent');
    const location = player.location;
    
    locationContent.innerHTML = `
        <div class="location-map">
            <div class="location-name mb-3">
                ${location.location_tuple.join(' - ')}
            </div>
            
            ${location.description ? `
                <div class="location-description mb-3">
                    <p>${location.description}</p>
                </div>
            ` : ''}
            
            <div class="accessible-locations">
                <h6>Accessible Locations:</h6>
                ${location.accessible_locations.length > 0 ? `
                    <div class="list-group">
                        ${location.accessible_locations.map(loc => `
                            <div class="accessible-location-item">
                                ${loc.join(' - ')}
                            </div>
                        `).join('')}
                    </div>
                ` : '<p>No accessible locations available</p>'}
            </div>
        </div>
    `;
}

// Load thoughts tab content
async function loadThoughtsTab(playerId) {
    try {
        const thoughtsContent = document.getElementById('thoughtsContent');
        thoughtsContent.innerHTML = '<div class="spinner-container"><div class="spinner-border" role="status"></div></div>';
        
        const result = await apiRequest(`/players/${playerId}/thoughts`);
        
        if (result.success) {
            const thoughts = result.data.thoughts;
            
            thoughtsContent.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5>Thought History</h5>
                    <button class="btn btn-primary btn-sm" id="addThoughtBtn">Add Thought</button>
                </div>
                
                <div id="thoughtsList">
                    ${thoughts.length > 0 ? thoughts.map(thought => `
                        <div class="thought-item">
                            <span class="thought-category thought-category-${thought.category}">${thought.category}</span>
                            <p>${thought.content}</p>
                            <div class="thought-timestamp">${formatDate(thought.timestamp)}</div>
                        </div>
                    `).join('') : '<p class="text-center">No thoughts recorded</p>'}
                </div>
            `;
            
            // Add event listener to add thought button
            document.getElementById('addThoughtBtn').addEventListener('click', () => showAddThoughtModal(playerId));
        }
    } catch (error) {
        console.error('Error loading thoughts:', error);
    }
}

// Load battles tab content
async function loadBattlesTab(playerId) {
    try {
        const battlesContent = document.getElementById('battlesContent');
        battlesContent.innerHTML = '<div class="spinner-container"><div class="spinner-border" role="status"></div></div>';
        
        const result = await apiRequest(`/players/${playerId}/battles`);
        
        if (result.success) {
            const battles = result.data.battles;
            
            battlesContent.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5>Battle History</h5>
                    <button class="btn btn-primary btn-sm" id="addBattleBtn">Add Battle</button>
                </div>
                
                <div id="battlesList">
                    ${battles.length > 0 ? battles.map(battle => `
                        <div class="battle-item">
                            <div class="d-flex justify-content-between align-items-center">
                                <h6>vs. ${battle.opponent_name}</h6>
                                ${battle.result ? `<span class="battle-result-${battle.result}">${battle.result.toUpperCase()}</span>` : '<span class="badge bg-secondary">In Progress</span>'}
                            </div>
                            <div class="small text-muted">
                                Started: ${formatDate(battle.start_time)}
                                ${battle.end_time ? ` | Ended: ${formatDate(battle.end_time)}` : ''}
                            </div>
                            <div class="mt-2">
                                <button class="btn btn-sm btn-outline-primary view-battle-btn" data-id="${battle.id}">View Details</button>
                            </div>
                        </div>
                    `).join('') : '<p class="text-center">No battles recorded</p>'}
                </div>
            `;
            
            // Add event listener to add battle button
            document.getElementById('addBattleBtn').addEventListener('click', () => showAddBattleModal(playerId));
            
            // Add event listeners to view battle buttons
            document.querySelectorAll('.view-battle-btn').forEach(btn => {
                btn.addEventListener('click', () => viewBattleDetails(playerId, btn.dataset.id));
            });
        }
    } catch (error) {
        console.error('Error loading battles:', error);
    }
}

// Load matchups tab content
async function loadMatchupsTab(playerId) {
    try {
        const matchupsContent = document.getElementById('matchupsContent');
        matchupsContent.innerHTML = '<div class="spinner-container"><div class="spinner-border" role="status"></div></div>';
        
        const result = await apiRequest(`/players/${playerId}/matchups`);
        
        if (result.success) {
            const matchups = result.data.matchups;
            const matchupKeys = Object.keys(matchups);
            
            matchupsContent.innerHTML = `
                <h5 class="mb-3">Matchup Records</h5>
                
                <div id="matchupsList">
                    ${matchupKeys.length > 0 ? matchupKeys.map(key => {
                        const matchup = matchups[key];
                        const totalBattles = matchup.wins + matchup.losses + matchup.draws;
                        const winRate = totalBattles > 0 ? ((matchup.wins / totalBattles) * 100).toFixed(1) : 0;
                        
                        return `
                            <div class="matchup-item">
                                <h6>${matchup.opponent_name}</h6>
                                <div class="matchup-record">
                                    <span class="matchup-wins">Wins: ${matchup.wins}</span>
                                    <span class="matchup-losses">Losses: ${matchup.losses}</span>
                                    <span class="matchup-draws">Draws: ${matchup.draws}</span>
                                </div>
                                <div class="progress mt-2" style="height: 10px;">
                                    <div class="progress-bar bg-success" role="progressbar" style="width: ${(matchup.wins / totalBattles) * 100}%"></div>
                                    <div class="progress-bar bg-danger" role="progressbar" style="width: ${(matchup.losses / totalBattles) * 100}%"></div>
                                    <div class="progress-bar bg-secondary" role="progressbar" style="width: ${(matchup.draws / totalBattles) * 100}%"></div>
                                </div>
                                <div class="small text-muted mt-2">
                                    Win Rate: ${winRate}%
                                    ${matchup.last_battle ? ` | Last Battle: ${formatDate(matchup.last_battle)}` : ''}
                                </div>
                            </div>
                        `;
                    }).join('') : '<p class="text-center">No matchup records</p>'}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading matchups:', error);
    }
}

// Show add thought modal
function showAddThoughtModal(playerId) {
    // Create modal if it doesn't exist
    if (!document.getElementById('addThoughtModal')) {
        const modalDiv = document.createElement('div');
        modalDiv.className = 'modal fade';
        modalDiv.id = 'addThoughtModal';
        modalDiv.setAttribute('tabindex', '-1');
        modalDiv.setAttribute('aria-hidden', 'true');
        
        modalDiv.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Add Thought</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="addThoughtForm">
                            <div class="mb-3">
                                <label for="thoughtContent" class="form-label">Thought Content</label>
                                <textarea class="form-control" id="thoughtContent" rows="4" required></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="thoughtCategory" class="form-label">Category</label>
                                <select class="form-select" id="thoughtCategory">
                                    <option value="general">General</option>
                                    <option value="battle">Battle</option>
                                    <option value="exploration">Exploration</option>
                                </select>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="saveThoughtBtn">Add Thought</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modalDiv);
    }
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('addThoughtModal'));
    modal.show();
    
    // Add event listener to save button
    document.getElementById('saveThoughtBtn').addEventListener('click', async () => {
        const content = document.getElementById('thoughtContent').value.trim();
        const category = document.getElementById('thoughtCategory').value;
        
        if (!content) {
            showAlert('Thought content is required', 'danger');
            return;
        }
        
        try {
            const result = await apiRequest(`/players/${playerId}/thoughts`, 'POST', {
                content,
                category
            });
            
            if (result.success) {
                showAlert('Thought added successfully', 'success');
                modal.hide();
                await loadThoughtsTab(playerId);
            }
        } catch (error) {
            console.error('Error adding thought:', error);
        }
    });
}

// Show add battle modal
function showAddBattleModal(playerId) {
    // Create modal if it doesn't exist
    if (!document.getElementById('addBattleModal')) {
        const modalDiv = document.createElement('div');
        modalDiv.className = 'modal fade';
        modalDiv.id = 'addBattleModal';
        modalDiv.setAttribute('tabindex', '-1');
        modalDiv.setAttribute('aria-hidden', 'true');
        
        modalDiv.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Start New Battle</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="addBattleForm">
                            <div class="mb-3">
                                <label for="opponentId" class="form-label">Opponent ID</label>
                                <input type="text" class="form-control" id="opponentId" required>
                            </div>
                            <div class="mb-3">
                                <label for="opponentName" class="form-label">Opponent Name</label>
                                <input type="text" class="form-control" id="opponentName" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="startBattleBtn">Start Battle</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modalDiv);
    }
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('addBattleModal'));
    modal.show();
    
    // Add event listener to start battle button
    document.getElementById('startBattleBtn').addEventListener('click', async () => {
        const opponentId = document.getElementById('opponentId').value.trim();
        const opponentName = document.getElementById('opponentName').value.trim();
        
        if (!opponentId || !opponentName) {
            showAlert('Opponent ID and name are required', 'danger');
            return;
        }
        
        try {
            const result = await apiRequest(`/players/${playerId}/battles`, 'POST', {
                opponent_id: opponentId,
                opponent_name: opponentName
            });
            
            if (result.success) {
                showAlert('Battle started successfully', 'success');
                modal.hide();
                await loadBattlesTab(playerId);
            }
        } catch (error) {
            console.error('Error starting battle:', error);
        }
    });
}

// View battle details
async function viewBattleDetails(playerId, battleId) {
    try {
        const result = await apiRequest(`/players/${playerId}/battles/${battleId}`);
        
        if (result.success) {
            const battle = result.data;
            
            // Create modal if it doesn't exist
            if (!document.getElementById('battleDetailsModal')) {
                const modalDiv = document.createElement('div');
                modalDiv.className = 'modal fade';
                modalDiv.id = 'battleDetailsModal';
                modalDiv.setAttribute('tabindex', '-1');
                modalDiv.setAttribute('aria-hidden', 'true');
                
                modalDiv.innerHTML = `
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="battleDetailsTitle">Battle Details</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body" id="battleDetailsContent">
                                <!-- Battle details will be loaded here -->
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <div id="battleResultBtns"></div>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modalDiv);
            }
            
            // Update modal content
            document.getElementById('battleDetailsTitle').textContent = `Battle vs. ${battle.opponent_name}`;
            
            const battleDetailsContent = document.getElementById('battleDetailsContent');
            battleDetailsContent.innerHTML = `
                <div class="row mb-3">
                    <div class="col-md-6">
                        <h6>Status</h6>
                        <p>${battle.result ? `<span class="battle-result-${battle.result}">${battle.result.toUpperCase()}</span>` : '<span class="badge bg-secondary">In Progress</span>'}</p>
                    </div>
                    <div class="col-md-6">
                        <h6>Timing</h6>
                        <p>
                            Started: ${formatDate(battle.start_time)}<br>
                            ${battle.end_time ? `Ended: ${formatDate(battle.end_time)}` : 'In progress'}
                        </p>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <h6>Your Team</h6>
                        <div class="list-group">
                            ${battle.player_team.map(pokemon => `
                                <div class="list-group-item">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <strong>${pokemon.name}</strong> (Lv. ${pokemon.level})
                                            <div>
                                                ${pokemon.types.map(type => 
                                                    `<span class="type-badge type-${type.toLowerCase()}">${type}</span>`
                                                ).join('')}
                                            </div>
                                        </div>
                                        <div>
                                            HP: ${pokemon.current_hp}/${pokemon.max_hp}
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h6>Opponent's Team</h6>
                        <div class="list-group">
                            ${battle.opponent_team.length > 0 ? battle.opponent_team.map(pokemon => {
                                if (!pokemon) return '<div class="list-group-item">Unknown Pokemon</div>';
                                
                                return `
                                    <div class="list-group-item">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <strong>${pokemon.name}</strong> (Lv. ${pokemon.level})
                                                <div>
                                                    ${pokemon.types.map(type => 
                                                        `<span class="type-badge type-${type.toLowerCase()}">${type}</span>`
                                                    ).join('')}
                                                </div>
                                            </div>
                                            <div>
                                                HP: ${pokemon.current_hp}/${pokemon.max_hp}
                                            </div>
                                        </div>
                                    </div>
                                `;
                            }).join('') : '<div class="list-group-item">No opponent Pokemon recorded</div>'}
                        </div>
                    </div>
                </div>
                
                ${battle.turns.length > 0 ? `
                    <h6 class="mt-4">Battle Log</h6>
                    <div class="battle-log p-3 bg-light" style="max-height: 300px; overflow-y: auto;">
                        ${battle.turns.map(turn => `
                            <div class="mb-2">
                                <strong>Turn ${turn.turn_number}:</strong>
                                <div>
                                    <span class="text-primary">You:</span> 
                                    ${formatBattleAction(turn.player_action)}
                                </div>
                                ${turn.opponent_action ? `
                                    <div>
                                        <span class="text-danger">Opponent:</span> 
                                        ${formatBattleAction(turn.opponent_action)}
                                    </div>
                                ` : ''}
                                ${turn.effects.length > 0 ? `
                                    <div class="small text-muted">
                                        ${turn.effects.join('<br>')}
                                    </div>
                                ` : ''}
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            `;
            
            // Add battle result buttons if battle is in progress
            const battleResultBtns = document.getElementById('battleResultBtns');
            battleResultBtns.innerHTML = '';
            
            if (!battle.result) {
                battleResultBtns.innerHTML = `
                    <button type="button" class="btn btn-success me-2" data-result="win">Win</button>
                    <button type="button" class="btn btn-danger me-2" data-result="loss">Loss</button>
                    <button type="button" class="btn btn-secondary" data-result="draw">Draw</button>
                `;
                
                // Add event listeners to result buttons
                battleResultBtns.querySelectorAll('button').forEach(btn => {
                    btn.addEventListener('click', async () => {
                        try {
                            const result = await apiRequest(`/players/${playerId}/battles/${battleId}`, 'PUT', btn.dataset.result);
                            
                            if (result.success) {
                                showAlert(`Battle result updated: ${btn.dataset.result}`, 'success');
                                
                                // Close modal and reload battles tab
                                const modal = bootstrap.Modal.getInstance(document.getElementById('battleDetailsModal'));
                                modal.hide();
                                
                                await loadBattlesTab(playerId);
                            }
                        } catch (error) {
                            console.error('Error updating battle result:', error);
                        }
                    });
                });
            }
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('battleDetailsModal'));
            modal.show();
        }
    } catch (error) {
        console.error('Error viewing battle details:', error);
    }
}

// Format battle action for display
function formatBattleAction(action) {
    if (!action) return 'No action';
    
    switch (action.action_type) {
        case 'move':
            return `Used move ${action.move_index + 1} with Pokemon ${action.pokemon_index + 1}${action.target_index !== null ? ` targeting position ${action.target_index + 1}` : ''}`;
        case 'switch':
            return `Switched to Pokemon ${action.pokemon_index + 1}`;
        case 'item':
            return `Used item ${action.item_name} on Pokemon ${action.pokemon_index + 1}`;
        case 'run':
            return 'Attempted to run';
        default:
            return `Unknown action: ${action.action_type}`;
    }
}

// Delete player
async function deletePlayer(playerId) {
    if (!confirm(`Are you sure you want to delete this player? This action cannot be undone.`)) {
        return;
    }
    
    try {
        const result = await apiRequest(`/players/${playerId}`, 'DELETE');
        
        if (result.success) {
            showAlert('Player deleted successfully', 'success');
            await loadPlayers();
        }
    } catch (error) {
        console.error('Error deleting player:', error);
    }
}
