"""
Karma System - Comprehensive moral alignment system affecting all interactions
Tracks player actions and determines how NPCs, other players, and the world treats them
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

class KarmaAlignment(Enum):
    PURE_SAINT = "pure_saint"          # 90-100 karma
    VIRTUOUS = "virtuous"              # 70-89 karma  
    GOOD = "good"                      # 50-69 karma
    NEUTRAL = "neutral"                # 25-49 karma
    SELFISH = "selfish"                # 10-24 karma
    CORRUPT = "corrupt"                # -10 to 9 karma
    EVIL = "evil"                      # -25 to -11 karma
    DARK_LORD = "dark_lord"            # -50 to -26 karma
    ABSOLUTE_EVIL = "absolute_evil"    # -100 to -51 karma

class KarmaActionType(Enum):
    BEAST_CARE = "beast_care"
    HELP_PLAYER = "help_player"
    PROTECT_INNOCENT = "protect_innocent"
    COMPLETE_QUEST = "complete_quest"
    DONATE_CHARITY = "donate_charity"
    HEAL_OTHERS = "heal_others"
    SHARE_KNOWLEDGE = "share_knowledge"
    
    KILL_INNOCENT = "kill_innocent"
    STEAL = "steal"
    LIE_DECEIVE = "lie_deceive"
    ABANDON_QUEST = "abandon_quest"
    HARM_BEAST = "harm_beast"
    BETRAY_PLAYER = "betray_player"
    USE_FORBIDDEN_POWER = "use_forbidden_power"

@dataclass
class KarmaAction:
    action_type: KarmaActionType
    karma_change: int
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    witnesses: List[str] = field(default_factory=list)
    location: str = ""
    target: Optional[str] = None

@dataclass
class PlayerReputation:
    player_id: str
    karma_score: int = 50
    alignment: KarmaAlignment = KarmaAlignment.NEUTRAL
    karma_history: List[KarmaAction] = field(default_factory=list)
    reputation_with_npcs: Dict[str, int] = field(default_factory=dict)
    reputation_with_factions: Dict[str, int] = field(default_factory=dict)
    titles: List[str] = field(default_factory=list)
    corruption_level: int = 0
    divine_favor: Dict[str, int] = field(default_factory=dict)

class KarmaSystem:
    def __init__(self):
        self.player_reputations: Dict[str, PlayerReputation] = {}
        self.karma_actions = {
            # Positive actions
            KarmaActionType.BEAST_CARE: 5,
            KarmaActionType.HELP_PLAYER: 10,
            KarmaActionType.PROTECT_INNOCENT: 15,
            KarmaActionType.COMPLETE_QUEST: 8,
            KarmaActionType.DONATE_CHARITY: 12,
            KarmaActionType.HEAL_OTHERS: 7,
            KarmaActionType.SHARE_KNOWLEDGE: 6,
            
            # Negative actions
            KarmaActionType.KILL_INNOCENT: -25,
            KarmaActionType.STEAL: -15,
            KarmaActionType.LIE_DECEIVE: -8,
            KarmaActionType.ABANDON_QUEST: -10,
            KarmaActionType.HARM_BEAST: -12,
            KarmaActionType.BETRAY_PLAYER: -20,
            KarmaActionType.USE_FORBIDDEN_POWER: -18
        }
        
        self.alignment_thresholds = {
            KarmaAlignment.PURE_SAINT: 90,
            KarmaAlignment.VIRTUOUS: 70,
            KarmaAlignment.GOOD: 50,
            KarmaAlignment.NEUTRAL: 25,
            KarmaAlignment.SELFISH: 10,
            KarmaAlignment.CORRUPT: -10,
            KarmaAlignment.EVIL: -25,
            KarmaAlignment.DARK_LORD: -50,
            KarmaAlignment.ABSOLUTE_EVIL: -100
        }
        
        # NPC reaction modifiers based on karma alignment
        self.npc_reaction_modifiers = {
            KarmaAlignment.PURE_SAINT: {
                "dialogue_tone": "reverent",
                "price_modifier": 0.5,  # 50% discount
                "quest_difficulty": 0.8,  # Easier quests
                "special_dialogue": True,
                "trust_level": 1.0
            },
            KarmaAlignment.VIRTUOUS: {
                "dialogue_tone": "respectful",
                "price_modifier": 0.8,
                "quest_difficulty": 0.9,
                "special_dialogue": True,
                "trust_level": 0.9
            },
            KarmaAlignment.GOOD: {
                "dialogue_tone": "friendly",
                "price_modifier": 0.9,
                "quest_difficulty": 1.0,
                "special_dialogue": False,
                "trust_level": 0.8
            },
            KarmaAlignment.NEUTRAL: {
                "dialogue_tone": "neutral",
                "price_modifier": 1.0,
                "quest_difficulty": 1.0,
                "special_dialogue": False,
                "trust_level": 0.5
            },
            KarmaAlignment.SELFISH: {
                "dialogue_tone": "cautious",
                "price_modifier": 1.2,
                "quest_difficulty": 1.1,
                "special_dialogue": False,
                "trust_level": 0.3
            },
            KarmaAlignment.CORRUPT: {
                "dialogue_tone": "suspicious",
                "price_modifier": 1.5,
                "quest_difficulty": 1.3,
                "special_dialogue": True,
                "trust_level": 0.2
            },
            KarmaAlignment.EVIL: {
                "dialogue_tone": "hostile",
                "price_modifier": 2.0,
                "quest_difficulty": 1.5,
                "special_dialogue": True,
                "trust_level": 0.1
            },
            KarmaAlignment.DARK_LORD: {
                "dialogue_tone": "fearful",
                "price_modifier": 3.0,
                "quest_difficulty": 2.0,
                "special_dialogue": True,
                "trust_level": 0.05
            },
            KarmaAlignment.ABSOLUTE_EVIL: {
                "dialogue_tone": "terrified",
                "price_modifier": 5.0,
                "quest_difficulty": 3.0,
                "special_dialogue": True,
                "trust_level": 0.01
            }
        }
    
    def get_player_reputation(self, player_id: str) -> PlayerReputation:
        """Get or create player reputation"""
        if player_id not in self.player_reputations:
            self.player_reputations[player_id] = PlayerReputation(player_id=player_id)
        
        return self.player_reputations[player_id]
    
    def record_karma_action(self, player_id: str, action_type: KarmaActionType, 
                           description: str = "", witnesses: List[str] = None,
                           location: str = "", target: str = None,
                           karma_multiplier: float = 1.0) -> Dict[str, Any]:
        """Record a karma action and update player's karma"""
        
        reputation = self.get_player_reputation(player_id)
        base_karma = self.karma_actions.get(action_type, 0)
        karma_change = int(base_karma * karma_multiplier)
        
        # Create karma action record
        action = KarmaAction(
            action_type=action_type,
            karma_change=karma_change,
            description=description or action_type.value.replace("_", " ").title(),
            witnesses=witnesses or [],
            location=location,
            target=target
        )
        
        # Update karma score
        old_karma = reputation.karma_score
        reputation.karma_score = max(-100, min(100, reputation.karma_score + karma_change))
        
        # Update alignment
        old_alignment = reputation.alignment
        reputation.alignment = self._calculate_alignment(reputation.karma_score)
        
        # Add to history
        reputation.karma_history.append(action)
        
        # Update corruption for forbidden actions
        if action_type == KarmaActionType.USE_FORBIDDEN_POWER:
            reputation.corruption_level = min(100, reputation.corruption_level + 5)
        
        # Calculate divine favor changes
        self._update_divine_favor(reputation, action_type, karma_change)
        
        # Update titles
        self._update_titles(reputation)
        
        # Determine world reaction
        world_reaction = self._get_world_reaction(action, old_alignment, reputation.alignment)
        
        return {
            "action_recorded": True,
            "karma_change": karma_change,
            "new_karma": reputation.karma_score,
            "old_alignment": old_alignment.value,
            "new_alignment": reputation.alignment.value,
            "alignment_changed": old_alignment != reputation.alignment,
            "corruption_level": reputation.corruption_level,
            "world_reaction": world_reaction,
            "action_description": action.description
        }
    
    def _calculate_alignment(self, karma_score: int) -> KarmaAlignment:
        """Calculate karma alignment based on score"""
        for alignment, threshold in self.alignment_thresholds.items():
            if karma_score >= threshold:
                return alignment
        return KarmaAlignment.ABSOLUTE_EVIL
    
    def _update_divine_favor(self, reputation: PlayerReputation, 
                           action_type: KarmaActionType, karma_change: int):
        """Update divine favor based on actions"""
        
        # Initialize divine favor if needed
        divine_beings = ["shiva", "vishnu", "brahma", "devi", "indra", "agni"]
        for deity in divine_beings:
            if deity not in reputation.divine_favor:
                reputation.divine_favor[deity] = 0
        
        # Update based on action type
        if action_type in [KarmaActionType.PROTECT_INNOCENT, KarmaActionType.HELP_PLAYER]:
            reputation.divine_favor["vishnu"] += karma_change // 2
        elif action_type in [KarmaActionType.SHARE_KNOWLEDGE, KarmaActionType.COMPLETE_QUEST]:
            reputation.divine_favor["brahma"] += karma_change // 2
        elif action_type == KarmaActionType.HEAL_OTHERS:
            reputation.divine_favor["devi"] += karma_change // 2
        elif action_type == KarmaActionType.USE_FORBIDDEN_POWER:
            # Lose favor with all good deities
            for deity in ["vishnu", "brahma", "devi"]:
                reputation.divine_favor[deity] += karma_change // 3  # Negative change
    
    def _update_titles(self, reputation: PlayerReputation):
        """Update player titles based on karma and actions"""
        
        # Clear old alignment-based titles
        alignment_titles = [
            "Saint", "Virtuous Soul", "Good Samaritan", "Neutral Wanderer",
            "Selfish Opportunist", "Corrupt Individual", "Evil Doer", 
            "Dark Lord", "Harbinger of Darkness"
        ]
        
        reputation.titles = [t for t in reputation.titles if t not in alignment_titles]
        
        # Add new alignment title
        if reputation.alignment == KarmaAlignment.PURE_SAINT:
            reputation.titles.append("Saint")
        elif reputation.alignment == KarmaAlignment.VIRTUOUS:
            reputation.titles.append("Virtuous Soul")
        elif reputation.alignment == KarmaAlignment.GOOD:
            reputation.titles.append("Good Samaritan")
        elif reputation.alignment == KarmaAlignment.NEUTRAL:
            reputation.titles.append("Neutral Wanderer")
        elif reputation.alignment == KarmaAlignment.SELFISH:
            reputation.titles.append("Selfish Opportunist")
        elif reputation.alignment == KarmaAlignment.CORRUPT:
            reputation.titles.append("Corrupt Individual")
        elif reputation.alignment == KarmaAlignment.EVIL:
            reputation.titles.append("Evil Doer")
        elif reputation.alignment == KarmaAlignment.DARK_LORD:
            reputation.titles.append("Dark Lord")
        elif reputation.alignment == KarmaAlignment.ABSOLUTE_EVIL:
            reputation.titles.append("Harbinger of Darkness")
        
        # Add special titles based on actions
        beast_care_actions = len([a for a in reputation.karma_history 
                                if a.action_type == KarmaActionType.BEAST_CARE])
        if beast_care_actions >= 50 and "Beast Friend" not in reputation.titles:
            reputation.titles.append("Beast Friend")
        
        help_actions = len([a for a in reputation.karma_history 
                          if a.action_type == KarmaActionType.HELP_PLAYER])
        if help_actions >= 25 and "Helper of Many" not in reputation.titles:
            reputation.titles.append("Helper of Many")
    
    def _get_world_reaction(self, action: KarmaAction, old_alignment: KarmaAlignment, 
                          new_alignment: KarmaAlignment) -> Dict[str, Any]:
        """Get world reaction to karma change"""
        
        reactions = []
        
        # Alignment change reactions
        if old_alignment != new_alignment:
            if new_alignment.value > old_alignment.value:  # Became more good
                reactions.append({
                    "type": "alignment_improvement",
                    "message": f"The world senses your growing virtue. You are now {new_alignment.value.replace('_', ' ').title()}!",
                    "effect": "NPCs view you more favorably"
                })
            else:  # Became more evil
                reactions.append({
                    "type": "alignment_degradation", 
                    "message": f"Darkness grows within you. You are now {new_alignment.value.replace('_', ' ').title()}.",
                    "effect": "NPCs become more suspicious and fearful"
                })
        
        # Specific action reactions
        if action.action_type == KarmaActionType.PROTECT_INNOCENT:
            reactions.append({
                "type": "heroic_deed",
                "message": "Your heroic actions are noticed by divine beings!",
                "effect": "Divine favor increased"
            })
        elif action.action_type == KarmaActionType.KILL_INNOCENT:
            reactions.append({
                "type": "evil_deed",
                "message": "The innocent cry out, and the heavens weep for your cruelty.",
                "effect": "Divine disfavor, guards may become hostile"
            })
        elif action.action_type == KarmaActionType.USE_FORBIDDEN_POWER:
            reactions.append({
                "type": "corruption",
                "message": "Forbidden power courses through you, but at what cost?",
                "effect": "Corruption increased, some NPCs fear you"
            })
        
        return {
            "reactions": reactions,
            "immediate_effects": self._get_immediate_effects(new_alignment)
        }
    
    def _get_immediate_effects(self, alignment: KarmaAlignment) -> List[str]:
        """Get immediate effects of current alignment"""
        effects = []
        
        if alignment == KarmaAlignment.PURE_SAINT:
            effects.extend([
                "Shop prices reduced by 50%",
                "NPCs offer additional help and information",
                "Some quests become easier",
                "Divine beasts may approach you",
                "Other players respect you more"
            ])
        elif alignment == KarmaAlignment.VIRTUOUS:
            effects.extend([
                "Shop prices reduced by 20%",
                "NPCs are more friendly and helpful",
                "Access to some exclusive good-aligned quests"
            ])
        elif alignment in [KarmaAlignment.CORRUPT, KarmaAlignment.EVIL]:
            effects.extend([
                "Shop prices increased by 50-100%",
                "NPCs are suspicious and may refuse service",
                "Guards watch you closely",
                "Access to dark/evil quests"
            ])
        elif alignment in [KarmaAlignment.DARK_LORD, KarmaAlignment.ABSOLUTE_EVIL]:
            effects.extend([
                "Shop prices increased by 200-400%",
                "Most NPCs fear you",
                "Guards may attack on sight in some areas",
                "Access to forbidden powers and evil quests",
                "Other players may avoid or challenge you"
            ])
        
        return effects
    
    def get_npc_reaction_to_player(self, player_id: str, npc_id: str) -> Dict[str, Any]:
        """Get how an NPC should react to a player based on karma"""
        
        reputation = self.get_player_reputation(player_id)
        base_reaction = self.npc_reaction_modifiers[reputation.alignment]
        
        # Get specific reputation with this NPC
        npc_reputation = reputation.reputation_with_npcs.get(npc_id, 0)
        
        # Modify base reaction with personal reputation
        reaction = base_reaction.copy()
        reaction["personal_reputation"] = npc_reputation
        reaction["karma_score"] = reputation.karma_score
        reaction["alignment"] = reputation.alignment.value
        reaction["titles"] = reputation.titles
        reaction["corruption_visible"] = reputation.corruption_level > 20
        
        # Special dialogue based on alignment
        if reputation.alignment == KarmaAlignment.PURE_SAINT:
            reaction["special_greeting"] = "Blessed one, your pure heart shines like the sun!"
        elif reputation.alignment == KarmaAlignment.DARK_LORD:
            reaction["special_greeting"] = "I... I sense great darkness within you. Please, do not harm me!"
        elif reputation.alignment == KarmaAlignment.ABSOLUTE_EVIL:
            reaction["special_greeting"] = "*trembles in fear* What... what do you want from me, dark one?"
        
        return reaction
    
    def get_karma_summary(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive karma summary for a player"""
        
        reputation = self.get_player_reputation(player_id)
        
        # Calculate recent karma trend
        recent_actions = [a for a in reputation.karma_history 
                         if a.timestamp > datetime.now() - timedelta(hours=24)]
        recent_karma_change = sum(a.karma_change for a in recent_actions)
        
        return {
            "player_id": player_id,
            "karma_score": reputation.karma_score,
            "alignment": {
                "current": reputation.alignment.value,
                "display_name": reputation.alignment.value.replace("_", " ").title(),
                "description": self._get_alignment_description(reputation.alignment)
            },
            "corruption_level": reputation.corruption_level,
            "titles": reputation.titles,
            "divine_favor": reputation.divine_favor,
            "recent_trend": {
                "karma_change_24h": recent_karma_change,
                "actions_count_24h": len(recent_actions),
                "trend": "improving" if recent_karma_change > 0 else "declining" if recent_karma_change < 0 else "stable"
            },
            "total_actions": len(reputation.karma_history),
            "npc_relations": len(reputation.reputation_with_npcs),
            "world_standing": self._get_world_standing(reputation.alignment)
        }
    
    def _get_alignment_description(self, alignment: KarmaAlignment) -> str:
        """Get description of alignment"""
        descriptions = {
            KarmaAlignment.PURE_SAINT: "A beacon of pure virtue, revered by all good beings",
            KarmaAlignment.VIRTUOUS: "A good-hearted individual who strives to help others", 
            KarmaAlignment.GOOD: "Generally kind and helpful, trusted by most people",
            KarmaAlignment.NEUTRAL: "Balanced in morality, neither particularly good nor evil",
            KarmaAlignment.SELFISH: "Focuses on personal gain, but not necessarily harmful",
            KarmaAlignment.CORRUPT: "Has fallen to temptation and acts selfishly",
            KarmaAlignment.EVIL: "Actively harmful and malicious toward others",
            KarmaAlignment.DARK_LORD: "A powerful force of evil, feared by all",
            KarmaAlignment.ABSOLUTE_EVIL: "Pure malevolence incarnate, avoided by all good beings"
        }
        return descriptions.get(alignment, "Unknown alignment")
    
    def _get_world_standing(self, alignment: KarmaAlignment) -> str:
        """Get player's standing in the world"""
        standings = {
            KarmaAlignment.PURE_SAINT: "Beloved Hero",
            KarmaAlignment.VIRTUOUS: "Respected Citizen",
            KarmaAlignment.GOOD: "Welcome Visitor", 
            KarmaAlignment.NEUTRAL: "Unknown Traveler",
            KarmaAlignment.SELFISH: "Watched Carefully",
            KarmaAlignment.CORRUPT: "Mistrusted Individual",
            KarmaAlignment.EVIL: "Feared Threat",
            KarmaAlignment.DARK_LORD: "Terror of the Realm",
            KarmaAlignment.ABSOLUTE_EVIL: "Nightmare Made Flesh"
        }
        return standings.get(alignment, "Unknown")

# Test the karma system
async def test_karma_system():
    """Test karma system functionality"""
    karma_system = KarmaSystem()
    
    print("=== KARMA SYSTEM TEST ===\n")
    
    # Test initial player reputation
    print("1. Testing initial reputation...")
    reputation = karma_system.get_player_reputation("test_player")
    print(f"Initial karma: {reputation.karma_score}, Alignment: {reputation.alignment.value}")
    
    # Test positive action
    print("\n2. Testing positive karma action...")
    result = karma_system.record_karma_action(
        "test_player", 
        KarmaActionType.HELP_PLAYER,
        "Helped another player defeat a difficult beast",
        witnesses=["player2", "player3"],
        location="Dark Forest"
    )
    print(f"Karma action result: {result}")
    
    # Test negative action
    print("\n3. Testing negative karma action...")
    result = karma_system.record_karma_action(
        "test_player",
        KarmaActionType.USE_FORBIDDEN_POWER,
        "Used dark magic to gain power",
        location="Forbidden Shrine"
    )
    print(f"Negative action result: {result}")
    
    # Test NPC reaction
    print("\n4. Testing NPC reaction...")
    npc_reaction = karma_system.get_npc_reaction_to_player("test_player", "arunima")
    print(f"NPC reaction: {npc_reaction}")
    
    # Test karma summary
    print("\n5. Testing karma summary...")
    summary = karma_system.get_karma_summary("test_player")
    print(f"Karma summary: {summary}")

if __name__ == "__main__":
    asyncio.run(test_karma_system())