import 'package:cloud_firestore/cloud_firestore.dart';

class Event {
  final String id;
  final String title;
  final String description;
  final DateTime dateTime;
  final String location;
  final String creatorId;
  final String creatorName;
  final List<String> attendeeIds;
  final String? imageUrl;
  final EventCategory category;
  final bool isPublic;
  final int maxAttendees;
  final DateTime createdAt;
  final DateTime updatedAt;

  Event({
    required this.id,
    required this.title,
    required this.description,
    required this.dateTime,
    required this.location,
    required this.creatorId,
    required this.creatorName,
    required this.attendeeIds,
    this.imageUrl,
    required this.category,
    this.isPublic = true,
    this.maxAttendees = 50,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Event.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return Event(
      id: doc.id,
      title: data['title'] ?? '',
      description: data['description'] ?? '',
      dateTime: (data['dateTime'] as Timestamp).toDate(),
      location: data['location'] ?? '',
      creatorId: data['creatorId'] ?? '',
      creatorName: data['creatorName'] ?? '',
      attendeeIds: List<String>.from(data['attendeeIds'] ?? []),
      imageUrl: data['imageUrl'],
      category: EventCategory.values.firstWhere(
        (e) => e.toString() == 'EventCategory.${data['category']}',
        orElse: () => EventCategory.social,
      ),
      isPublic: data['isPublic'] ?? true,
      maxAttendees: data['maxAttendees'] ?? 50,
      createdAt: (data['createdAt'] as Timestamp).toDate(),
      updatedAt: (data['updatedAt'] as Timestamp).toDate(),
    );
  }

  Map<String, dynamic> toFirestore() {
    return {
      'title': title,
      'description': description,
      'dateTime': Timestamp.fromDate(dateTime),
      'location': location,
      'creatorId': creatorId,
      'creatorName': creatorName,
      'attendeeIds': attendeeIds,
      'imageUrl': imageUrl,
      'category': category.toString().split('.').last,
      'isPublic': isPublic,
      'maxAttendees': maxAttendees,
      'createdAt': Timestamp.fromDate(createdAt),
      'updatedAt': Timestamp.fromDate(updatedAt),
    };
  }

  Event copyWith({
    String? id,
    String? title,
    String? description,
    DateTime? dateTime,
    String? location,
    String? creatorId,
    String? creatorName,
    List<String>? attendeeIds,
    String? imageUrl,
    EventCategory? category,
    bool? isPublic,
    int? maxAttendees,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Event(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      dateTime: dateTime ?? this.dateTime,
      location: location ?? this.location,
      creatorId: creatorId ?? this.creatorId,
      creatorName: creatorName ?? this.creatorName,
      attendeeIds: attendeeIds ?? this.attendeeIds,
      imageUrl: imageUrl ?? this.imageUrl,
      category: category ?? this.category,
      isPublic: isPublic ?? this.isPublic,
      maxAttendees: maxAttendees ?? this.maxAttendees,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  bool get isFull => attendeeIds.length >= maxAttendees;
  bool get isPast => dateTime.isBefore(DateTime.now());
  int get availableSpots => maxAttendees - attendeeIds.length;
}

enum EventCategory {
  social,
  sports,
  music,
  food,
  outdoor,
  gaming,
  education,
  business,
  art,
  other,
}

extension EventCategoryExtension on EventCategory {
  String get displayName {
    switch (this) {
      case EventCategory.social:
        return 'Social';
      case EventCategory.sports:
        return 'Sports';
      case EventCategory.music:
        return 'Music';
      case EventCategory.food:
        return 'Food & Drinks';
      case EventCategory.outdoor:
        return 'Outdoor';
      case EventCategory.gaming:
        return 'Gaming';
      case EventCategory.education:
        return 'Education';
      case EventCategory.business:
        return 'Business';
      case EventCategory.art:
        return 'Art & Culture';
      case EventCategory.other:
        return 'Other';
    }
  }

  String get emoji {
    switch (this) {
      case EventCategory.social:
        return '🎉';
      case EventCategory.sports:
        return '⚽';
      case EventCategory.music:
        return '🎵';
      case EventCategory.food:
        return '🍕';
      case EventCategory.outdoor:
        return '🌲';
      case EventCategory.gaming:
        return '🎮';
      case EventCategory.education:
        return '📚';
      case EventCategory.business:
        return '💼';
      case EventCategory.art:
        return '🎨';
      case EventCategory.other:
        return '📅';
    }
  }
}
